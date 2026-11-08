// LeetCode #1506: Find Root of N-Ary Tree -- the benchmark, the same
// algorithm as root.kara: all values less all children's values.
package main

import "fmt"

type Node struct {
	val      int64
	children []*Node
}

func findRoot(nodes []*Node) *Node {
	var total int64
	for _, node := range nodes {
		total += node.val
		for _, child := range node.children {
			total -= child.val
		}
	}
	for _, node := range nodes {
		if node.val == total {
			return node
		}
	}
	return nodes[0]
}

var seed int64 = 1506

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func randomTree(most int64) []*Node {
	n := int(nextRandom()%most + 1)
	vals := []int64{}
	seen := map[int64]bool{}
	for len(vals) < n {
		a := nextRandom()
		v := (a*65536 + nextRandom()) % 50001
		if !seen[v] {
			seen[v] = true
			vals = append(vals, v)
		}
	}
	kids := make([][]int, n)
	for i := 1; i < n; i++ {
		p := nextRandom() % int64(i)
		kids[p] = append(kids[p], i)
	}
	nodes := make([]*Node, n)
	for i := n - 1; i >= 0; i-- {
		children := make([]*Node, 0, len(kids[i]))
		for _, c := range kids[i] {
			children = append(children, nodes[c])
		}
		nodes[i] = &Node{val: vals[i], children: children}
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % int64(i+1)
		nodes[i], nodes[j] = nodes[j], nodes[i]
	}
	return nodes
}

func main() {
	trees := make([][]*Node, 20)
	for t := range trees {
		trees[t] = randomTree(50000)
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, nodes := range trees {
			copied := append([]*Node(nil), nodes...)
			check = mix(check, findRoot(copied).val)
		}
	}
	fmt.Printf("200 roots over 20 trees of up to 50000 nodes: checksum %d\n", check)
}
