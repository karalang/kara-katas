// Benchmark for #427: mirror of quad_tree.kara (divide, then merge).
// Every node is a heap pointer, left to Go's collector.
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Quad struct {
	leaf bool
	val  bool
	kids [4]*Quad // top left, top right, bottom left, bottom right
}

func build(grid [][]int64, row, col, size int64) *Quad {
	if size == 1 {
		return &Quad{leaf: true, val: grid[row][col] == 1}
	}
	half := size / 2
	tl := build(grid, row, col, half)
	tr := build(grid, row, col+half, half)
	bl := build(grid, row+half, col, half)
	br := build(grid, row+half, col+half, half)
	if tl.leaf && tr.leaf && bl.leaf && br.leaf && tl.val == tr.val && tr.val == bl.val && bl.val == br.val {
		return &Quad{leaf: true, val: tl.val}
	}
	return &Quad{kids: [4]*Quad{tl, tr, bl, br}}
}

func construct(grid [][]int64) *Quad {
	return build(grid, 0, 0, int64(len(grid)))
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func count(q *Quad) int64 {
	if q.leaf {
		return 1
	}
	return 1 + count(q.kids[0]) + count(q.kids[1]) + count(q.kids[2]) + count(q.kids[3])
}

func main() {
	n := int64(64)
	rounds := int64(20000)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(427)
	grid := make([][]int64, n)
	for i := range grid {
		grid[i] = make([]int64, n)
	}
	total := int64(0)
	checksum := int64(0)
	for i := int64(0); i < rounds; i++ {
		size := int64(1) << (step(&seed) % 7)
		top := step(&seed) % (n / size) * size
		left := step(&seed) % (n / size) * size
		v := step(&seed) % 2
		for r := top; r < top+size; r++ {
			for c := left; c < left+size; c++ {
				grid[r][c] = v
			}
		}
		r := step(&seed) % n
		c := step(&seed) % n
		grid[r][c] = 1 - grid[r][c]
		nodes := count(construct(grid))
		total += nodes
		checksum = (checksum*31 + nodes) % 1000000007
	}
	fmt.Printf("%d rounds on a %d by %d grid: %d nodes, checksum %d\n", rounds, n, n, total, checksum)
}
