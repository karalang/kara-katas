// LeetCode #1522: Diameter of N-Ary Tree -- bench: the ★ arm over 1000
// random trees of 1 to 2000 nodes, built once and answered 20 times.
package main

import "fmt"

type Node struct {
	val      int64
	children []*Node
}

func height(node *Node, best *int64) int64 {
	var first, second int64
	for _, child := range node.children {
		h := height(child, best) + 1
		if h > first {
			second = first
			first = h
		} else if h > second {
			second = h
		}
	}
	if first+second > *best {
		*best = first + second
	}
	return first
}

func diameter(root *Node) int64 {
	var best int64
	height(root, &best)
	return best
}

func build(vals []int64, kids [][]int64) *Node {
	n := len(vals)
	made := make([]*Node, n)
	for i := n - 1; i >= 0; i-- {
		children := make([]*Node, 0, len(kids[i]))
		for _, c := range kids[i] {
			children = append(children, made[c])
		}
		made[i] = &Node{val: vals[i], children: children}
	}
	return made[0]
}

var seed int64 = 1522

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	const count = 1000
	trees := make([]*Node, 0, count)
	for t := 0; t < count; t++ {
		n := nextRandom()%2000 + 1
		window := nextRandom()%64 + 1
		vals := make([]int64, 0, n)
		kids := make([][]int64, n)
		for i := int64(0); i < n; i++ {
			vals = append(vals, nextRandom()%1000)
			if i > 0 {
				span := i
				if window < span {
					span = window
				}
				p := i - 1 - nextRandom()%span
				kids[p] = append(kids[p], i)
			}
		}
		trees = append(trees, build(vals, kids))
	}
	var check, total int64
	for pass := 0; pass < 20; pass++ {
		for _, tree := range trees {
			d := diameter(tree)
			total += d
			check = mix(check, d)
		}
	}
	fmt.Printf("20 passes over 1000 trees of up to 2000 nodes: diameters sum to %d, checksum %d\n", total, check)
}
