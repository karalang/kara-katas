// LeetCode #1382 bench -- Go: the ★ arm: the values read off in order,
// then a new tree built with the middle value at the root and each half
// built the same way beneath it.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func valuesInOrder(node *TreeNode, values *[]int32) {
	if node == nil {
		return
	}
	valuesInOrder(node.Left, values)
	*values = append(*values, node.Val)
	valuesInOrder(node.Right, values)
}

func build(values []int32, lo, hi int) *TreeNode {
	if lo >= hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &TreeNode{Val: values[mid], Left: build(values, lo, mid), Right: build(values, mid+1, hi)}
}

func balanceBST(root *TreeNode) *TreeNode {
	var values []int32
	valuesInOrder(root, &values)
	return build(values, 0, len(values))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func searchTree(values []int32) *TreeNode {
	root := &TreeNode{Val: values[0]}
	for _, v := range values[1:] {
		at := root
		for {
			next := &at.Right
			if v < at.Val {
				next = &at.Left
			}
			if *next != nil {
				at = *next
			} else {
				*next = &TreeNode{Val: v}
				break
			}
		}
	}
	return root
}

func main() {
	seed := int64(1382)
	trees := make([]*TreeNode, 0, 10)
	for t := 0; t < 10; t++ {
		step := 1 + nextRandom(&seed)%99990
		start := nextRandom(&seed) % 99991
		values := make([]int32, 10000)
		for k := int64(0); k < 10000; k++ {
			values[k] = int32(1 + (start+k*step)%99991)
		}
		for i := 9999; i >= 1; i-- {
			j := nextRandom(&seed) % int64(i+1)
			values[i], values[j] = values[j], values[i]
		}
		trees = append(trees, searchTree(values))
	}
	check := int64(0)
	for round := 0; round < 500; round++ {
		t := (check + nextRandom(&seed)) % 10
		balanced := balanceBST(trees[t])
		for at := balanced; at != nil; {
			check = (check*131 + int64(at.Val)) % 1000000007
			if nextRandom(&seed)%2 == 0 {
				at = at.Left
			} else {
				at = at.Right
			}
		}
		trees[t] = balanced
	}
	fmt.Printf("500 rounds over 10 trees of 10000 nodes: checksum %d\n", check)
}
