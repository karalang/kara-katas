// Benchmark for #545: Go mirror of the ★ arm (three walks); see
// ../boundary_of_binary_tree.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func isLeaf(n *TreeNode) bool { return n.Left == nil && n.Right == nil }

func leaves(node *TreeNode, out *[]int64) {
	if node == nil {
		return
	}
	if isLeaf(node) {
		*out = append(*out, node.Val)
	} else {
		leaves(node.Left, out)
		leaves(node.Right, out)
	}
}

func boundaryOfBinaryTree(r *TreeNode) []int64 {
	out := []int64{}
	if r == nil {
		return out
	}
	out = append(out, r.Val)
	if isLeaf(r) {
		return out
	}
	for n := r.Left; n != nil && !isLeaf(n); {
		out = append(out, n.Val)
		if n.Left != nil {
			n = n.Left
		} else {
			n = n.Right
		}
	}
	leaves(r.Left, &out)
	leaves(r.Right, &out)
	right := []int64{}
	for n := r.Right; n != nil && !isLeaf(n); {
		right = append(right, n.Val)
		if n.Right != nil {
			n = n.Right
		} else {
			n = n.Left
		}
	}
	for i := len(right) - 1; i >= 0; i-- {
		out = append(out, right[i])
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20 random trees of 10,000 nodes (the problem's most) with values
	// from -1,000 to 1,000, each new node walking down from the root and
	// going left with chance 50 to 88 in 100, built once, the nodes kept
	// in the order they were added. Then 200 times over every tree the
	// subtree at one of its first 16 nodes, picked by the round and the
	// tree, is answered; every value on the boundary goes into the
	// checksum.
	trees := 20
	seed := int64(545)
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
	for r := 0; r < 200; r++ {
		for t := 0; t < trees; t++ {
			b := boundaryOfBinaryTree(all[t][(r*37+t*11)%16])
			total += int64(len(b))
			for _, v := range b {
				checksum = (checksum*31 + v + 1001) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees, 200 times each: %d on the boundary, checksum %d\n", trees, total, checksum)
}
