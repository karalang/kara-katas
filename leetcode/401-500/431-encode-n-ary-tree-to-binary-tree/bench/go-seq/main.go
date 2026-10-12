// Benchmark for #431: mirror of encode.kara (left child, right sibling).
// Go's collector frees the trees.
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	val      int64
	children []*Node
}

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func encodeNode(node *Node) *TreeNode {
	t := &TreeNode{val: node.val}
	var prev *TreeNode
	for _, child := range node.children {
		c := encodeNode(child)
		if prev != nil {
			prev.right = c
		} else {
			t.left = c
		}
		prev = c
	}
	return t
}

func decodeNode(t *TreeNode) *Node {
	n := &Node{val: t.val}
	for c := t.left; c != nil; c = c.right {
		n.children = append(n.children, decodeNode(c))
	}
	return n
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func buildRandom(i int, vals []int64, kids [][]int) *Node {
	n := &Node{val: vals[i]}
	for _, k := range kids[i] {
		n.children = append(n.children, buildRandom(k, vals, kids))
	}
	return n
}

func fold(node *Node, count, checksum *int64) {
	*count++
	*checksum = (*checksum*31 + node.val) % 1000000007
	for _, child := range node.children {
		fold(child, count, checksum)
	}
}

func main() {
	n := 10000
	rounds := int64(100)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(431)
	var count, checksum int64
	for r := int64(0); r < rounds; r++ {
		reach := 10 + step(&seed)%1000
		vals := make([]int64, 0, n)
		kids := make([][]int, n)
		for i := 0; i < n; i++ {
			vals = append(vals, step(&seed)%10001)
			if i > 0 {
				lim := int64(i)
				if reach < lim {
					lim = reach
				}
				back := 1 + step(&seed)%lim
				kids[i-int(back)] = append(kids[i-int(back)], i)
			}
		}
		back := decodeNode(encodeNode(buildRandom(0, vals, kids)))
		fold(back, &count, &checksum)
	}
	fmt.Printf("%d rounds of %d nodes: %d decoded, checksum %d\n", rounds, n, count, checksum)
}
