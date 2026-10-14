// Benchmark for #558: Go mirror of the ★ arm (recursion, then a merge);
// see ../quad_tree_or.kara. A node is a pointer to a struct, collected by
// the garbage collector; the answer shares the subtrees it keeps with
// the two trees.
package main

import "fmt"

type Quad struct {
	leaf bool
	val  bool
	kids [4]*Quad // top left, top right, bottom left, bottom right
}

func merge(k [4]*Quad) *Quad {
	if k[0].leaf && k[1].leaf && k[2].leaf && k[3].leaf && k[0].val == k[1].val &&
		k[1].val == k[2].val && k[2].val == k[3].val {
		return &Quad{leaf: true, val: k[0].val}
	}
	return &Quad{val: true, kids: k}
}

func intersect(a, b *Quad) *Quad {
	if a.leaf {
		if a.val {
			return a
		}
		return b
	}
	if b.leaf {
		if b.val {
			return b
		}
		return a
	}
	var k [4]*Quad
	for i := 0; i < 4; i++ {
		k[i] = intersect(a.kids[i], b.kids[i])
	}
	return merge(k)
}

// ---- benchmark --------------------------------------------------------------

const n = 64

func build(grid [][]int64, row, col, size int) *Quad {
	if size == 1 {
		return &Quad{leaf: true, val: grid[row][col] == 1}
	}
	half := size / 2
	return merge([4]*Quad{
		build(grid, row, col, half),
		build(grid, row, col+half, half),
		build(grid, row+half, col, half),
		build(grid, row+half, col+half, half),
	})
}

func count(q *Quad) int64 {
	if q.leaf {
		return 1
	}
	return 1 + count(q.kids[0]) + count(q.kids[1]) + count(q.kids[2]) + count(q.kids[3])
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	countTrees, rounds := 200, 300
	seed := int64(558)
	trees := make([]*Quad, 0, countTrees)
	for t := 0; t < countTrees; t++ {
		block := 1 << (step(&seed) % 5)
		grid := make([][]int64, n)
		for r := range grid {
			grid[r] = make([]int64, n)
		}
		for br := 0; br < n/block; br++ {
			for bc := 0; bc < n/block; bc++ {
				var v int64
				if step(&seed)%3 == 0 {
					v = 1
				}
				for r := 0; r < block; r++ {
					for c := 0; c < block; c++ {
						grid[br*block+r][bc*block+c] = v
					}
				}
			}
		}
		for f := 0; f < 40; f++ {
			r := step(&seed) % n
			c := step(&seed) % n
			grid[r][c] = 1 - grid[r][c]
		}
		trees = append(trees, build(grid, 0, 0, n))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for i := 0; i < countTrees; i++ {
			other := (i*7 + round + 1) % countTrees
			nodes := count(intersect(trees[i], trees[other]))
			total += nodes
			checksum = (checksum*31 + nodes) % 1000000007
		}
	}
	fmt.Printf("%d trees, %d rounds: %d nodes, checksum %d\n", countTrees, rounds, total, checksum)
}
