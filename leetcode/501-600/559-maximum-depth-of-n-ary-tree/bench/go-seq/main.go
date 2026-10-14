// Benchmark for #559: Go mirror of the ★ arm (recursion); see
// ../maximum_depth.kara. A node holds its children in a slice of nodes,
// appended to as the Kāra Vec[Node] is pushed to.
package main

import "fmt"

type Node struct {
	val      int64
	children []Node
}

func depth(node *Node) int64 {
	var deepest int64
	for i := range node.children {
		if d := depth(&node.children[i]); d > deepest {
			deepest = d
		}
	}
	return deepest + 1
}

func maxDepth(root *Node) int64 {
	if root == nil {
		return 0
	}
	return depth(root)
}

// ---- benchmark --------------------------------------------------------------

func buildRandom(i int, vals []int64, kids [][]int) Node {
	children := []Node{}
	for _, k := range kids[i] {
		children = append(children, buildRandom(k, vals, kids))
	}
	return Node{val: vals[i], children: children}
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	n, count, rounds := 10000, 100, 50
	seed := int64(559)
	trees := make([]*Node, 0, count)
	for t := 0; t < count; t++ {
		reach := 2 + step(&seed)%1000
		vals := make([]int64, 0, n)
		kids := make([][]int, 0, n)
		for i := 0; i < n; i++ {
			vals = append(vals, step(&seed)%10001)
			kids = append(kids, []int{})
			if i > 0 {
				m := int64(i)
				if reach < m {
					m = reach
				}
				back := 1 + int(step(&seed)%m)
				kids[i-back] = append(kids[i-back], i)
			}
		}
		root := buildRandom(0, vals, kids)
		trees = append(trees, &root)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			d := maxDepth(trees[(round*7+g)%count])
			total += d
			checksum = (checksum*31 + d) % 1000000007
		}
	}
	fmt.Printf("%d trees of %d nodes, %d rounds: depths sum to %d, checksum %d\n", count, n, rounds, total, checksum)
}
