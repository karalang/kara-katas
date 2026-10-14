// Benchmark for #543: Go mirror of the ★ arm (heights, recursively); see
// ../diameter_of_binary_tree.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func height(node *TreeNode, best *int64) int64 {
	if node == nil {
		return 0
	}
	l := height(node.Left, best)
	r := height(node.Right, best)
	if l+r > *best {
		*best = l + r
	}
	return 1 + max(l, r)
}

func diameterOfBinaryTree(root *TreeNode) int64 {
	var best int64
	height(root, &best)
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20 random trees of 10,000 nodes (the problem's most), each new
	// node walking down from the root and going left with chance 50 to
	// 88 in 100, built once, the nodes kept in the order they were
	// added. Then 200 times over every tree the subtree at one of its
	// first 16 nodes, picked by the round and the tree, is answered.
	trees := 20
	seed := int64(543)
	all := make([][]*TreeNode, trees)
	for g := 0; g < trees; g++ {
		lean := int64(50 + 2*g)
		root := &TreeNode{Val: nextRandom(&seed)%201 - 100}
		nodes := []*TreeNode{root}
		for i := 1; i < 10000; i++ {
			c := &TreeNode{Val: nextRandom(&seed)%201 - 100}
			node := root
			for {
				if nextRandom(&seed)%100 < lean {
					if node.Left != nil {
						node = node.Left
					} else {
						node.Left = c
						break
					}
				} else {
					if node.Right != nil {
						node = node.Right
					} else {
						node.Right = c
						break
					}
				}
			}
			nodes = append(nodes, c)
		}
		all[g] = nodes
	}
	var total, checksum int64
	for r := 0; r < 200; r++ {
		for t := 0; t < trees; t++ {
			d := diameterOfBinaryTree(all[t][(r*37+t*11)%16])
			total += d
			checksum = (checksum*31 + d) % 1000000007
		}
	}
	fmt.Printf("%d trees, 200 times each: diameters %d, checksum %d\n", trees, total, checksum)
}
