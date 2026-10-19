// Benchmark for #776: Split BST -- mirror of the ★ arm (recursive), with
// the same workload as split_bst.kara.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func splitBST(root *TreeNode, target int64) (*TreeNode, *TreeNode) {
	if root == nil {
		return nil, nil
	}
	if root.val <= target {
		small, large := splitBST(root.right, target)
		root.right = small
		return root, large
	}
	small, large := splitBST(root.left, target)
	root.left = large
	return small, root
}

func insert(root *TreeNode, v int64) *TreeNode {
	fresh := &TreeNode{val: v}
	if root == nil {
		return fresh
	}
	node := root
	for {
		if v < node.val {
			if node.left == nil {
				node.left = fresh
				break
			}
			node = node.left
		} else {
			if node.right == nil {
				node.right = fresh
				break
			}
			node = node.right
		}
	}
	return root
}

func weigh(root *TreeNode, depth int64) int64 {
	if root == nil {
		return 0
	}
	return root.val*depth + weigh(root.left, depth+1) + weigh(root.right, depth+1)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	seed := int64(776)
	orders := make([][]int64, 0, count)
	targets := make([]int64, 0, count)
	for g := 0; g < count; g++ {
		used := map[int64]bool{}
		values := make([]int64, 0, 50)
		for len(values) < 50 {
			v := nextRandom(&seed) % 1001
			if !used[v] {
				used[v] = true
				values = append(values, v)
			}
		}
		orders = append(orders, values)
		targets = append(targets, nextRandom(&seed)%1001)
	}
	checksum := int64(0)
	for round := 0; round < 200000; round++ {
		g := round % count
		var root *TreeNode
		for _, v := range orders[g] {
			root = insert(root, v)
		}
		small, large := splitBST(root, targets[g])
		checksum = (checksum*31 + weigh(small, 1) + 3*weigh(large, 1)) % 1000000007
	}
	fmt.Printf("200000 rounds of 50 values: checksum %d\n", checksum)
}
