// Benchmark for #663: the subtree sums, listed, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func subtreeSum(node *TreeNode, sums *[]int64) int64 {
	if node == nil {
		return 0
	}
	s := node.val + subtreeSum(node.left, sums) + subtreeSum(node.right, sums)
	*sums = append(*sums, s)
	return s
}

func checkEqualTree(root *TreeNode) bool {
	var sums []int64
	total := subtreeSum(root, &sums)
	if total%2 != 0 {
		return false
	}
	sums = sums[:len(sums)-1]
	for _, s := range sums {
		if s == total/2 {
			return true
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func leaf(v int64) *TreeNode {
	return &TreeNode{val: v}
}

func grownTree(count int64, seed *int64) *TreeNode {
	root := leaf(nextRandom(seed)%200001 - 100000)
	for i := int64(1); i < count; i++ {
		at := root
		placed := false
		for !placed {
			if nextRandom(seed)%2 == 0 {
				if at.left != nil {
					at = at.left
				} else {
					at.left = leaf(nextRandom(seed)%200001 - 100000)
					placed = true
				}
			} else {
				if at.right != nil {
					at = at.right
				} else {
					at.right = leaf(nextRandom(seed)%200001 - 100000)
					placed = true
				}
			}
		}
	}
	return root
}

func copyTree(node *TreeNode) *TreeNode {
	if node == nil {
		return nil
	}
	return &TreeNode{val: node.val, left: copyTree(node.left), right: copyTree(node.right)}
}

func main() {
	seed := int64(663)
	trees := make([]*TreeNode, 0, 8)
	for i := 0; i < 4; i++ {
		trees = append(trees, grownTree(10000, &seed))
		root := leaf(0)
		root.left = grownTree(4999, &seed)
		root.right = copyTree(root.left)
		trees = append(trees, root)
	}
	rounds := int64(4000)
	var split, sum int64
	for r := int64(0); r < rounds; r++ {
		ok := checkEqualTree(trees[r%8])
		b := int64(0)
		if ok {
			split++
			b = 1
		}
		sum = (sum*31 + r*2 + b) % 1000000007
	}
	fmt.Printf("8 trees of 10000 nodes, %d rounds: %d split, checksum %d\n", rounds, split, sum)
}
