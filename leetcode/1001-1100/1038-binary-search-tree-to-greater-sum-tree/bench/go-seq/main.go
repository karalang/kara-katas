// LeetCode #1038: Binary Search Tree to Greater Sum Tree -- bench
// Mirrors ../../gst.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func addGreater(n *TreeNode, above int64) int64 {
	if n == nil {
		return above
	}
	total := addGreater(n.right, above) + n.val
	n.val = total
	return addGreater(n.left, total)
}

func bstToGst(root *TreeNode) *TreeNode {
	addGreater(root, 0)
	return root
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

// A search tree of the keys, inserted in the order given; every node is
// also listed, in the same order.
func build(keys []int64) (*TreeNode, []*TreeNode) {
	root := &TreeNode{val: keys[0]}
	nodes := []*TreeNode{root}
	for _, v := range keys[1:] {
		fresh := &TreeNode{val: v}
		nodes = append(nodes, fresh)
		node := root
		for {
			if v < node.val {
				if node.left != nil {
					node = node.left
				} else {
					node.left = fresh
					break
				}
			} else {
				if node.right != nil {
					node = node.right
				} else {
					node.right = fresh
					break
				}
			}
		}
	}
	return root, nodes
}

func main() {
	const trees, rounds = 10000, 50
	seed := int64(1038)
	pool := make([]int64, 101)
	for v := range pool {
		pool[v] = int64(v)
	}
	roots := make([]*TreeNode, trees)
	lists := make([][]*TreeNode, trees)
	originals := make([][]int64, trees)
	for t := 0; t < trees; t++ {
		for i := 0; i < 100; i++ {
			j := i + int(nextRandom(&seed)%int64(101-i))
			pool[i], pool[j] = pool[j], pool[i]
		}
		keys := append([]int64(nil), pool[:100]...)
		roots[t], lists[t] = build(keys)
		originals[t] = keys
	}
	total := int64(0)
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for t := 0; t < trees; t++ {
			for i, n := range lists[t] {
				n.val = originals[t][i]
			}
			top := bstToGst(roots[t]).val
			total += top
			check = (check*31 + top + 1000) % 1000000007
		}
	}
	fmt.Printf("%d trees of 100 keys, %d rounds: total %d, checksum %d\n", trees, rounds, total, check)
}
