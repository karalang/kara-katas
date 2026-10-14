// Benchmark for #563: Go mirror of the ★ arm (subtree sums, recursively);
// see ../find_tilt.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func subtreeSum(node *TreeNode, total *int64) int64 {
	if node == nil {
		return 0
	}
	l := subtreeSum(node.Left, total)
	r := subtreeSum(node.Right, total)
	if l > r {
		*total += l - r
	} else {
		*total += r - l
	}
	return node.Val + l + r
}

func findTilt(root *TreeNode) int64 {
	var total int64
	subtreeSum(root, &total)
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20 random trees of 10,000 nodes (the problem's most), each new
	// node walking down from the root and going left with chance 50 to
	// 88 in 100, built once, the nodes kept in the order they were
	// added. Then 1,000 times over every tree the subtree at one of its
	// first 16 nodes, picked by the round and the tree, is answered.
	trees := 20
	seed := int64(563)
	all := make([][]*TreeNode, trees)
	for g := 0; g < trees; g++ {
		lean := int64(50 + 2*g)
		root := &TreeNode{Val: nextRandom(&seed)%2001 - 1000}
		nodes := []*TreeNode{root}
		for i := 1; i < 10000; i++ {
			c := &TreeNode{Val: nextRandom(&seed)%2001 - 1000}
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
	for r := 0; r < 1000; r++ {
		for t := 0; t < trees; t++ {
			d := findTilt(all[t][(r*37+t*11)%16])
			total += d
			checksum = (checksum*31 + d) % 1000000007
		}
	}
	fmt.Printf("%d trees, 1000 times each: tilts %d, checksum %d\n", trees, total, checksum)
}
