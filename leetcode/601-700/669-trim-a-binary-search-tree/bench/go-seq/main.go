// Benchmark for #669: recursion, in place, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func trimBST(root *TreeNode, low, high int64) *TreeNode {
	if root == nil {
		return nil
	}
	if root.Val < low {
		return trimBST(root.Right, low, high)
	}
	if root.Val > high {
		return trimBST(root.Left, low, high)
	}
	root.Left = trimBST(root.Left, low, high)
	root.Right = trimBST(root.Right, low, high)
	return root
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func bst(values []int64) *TreeNode {
	root := &TreeNode{Val: values[0]}
	for _, v := range values[1:] {
		at := root
		for {
			if v < at.Val {
				if at.Left == nil {
					at.Left = &TreeNode{Val: v}
					break
				}
				at = at.Left
			} else {
				if at.Right == nil {
					at.Right = &TreeNode{Val: v}
					break
				}
				at = at.Right
			}
		}
	}
	return root
}

func checksum(root *TreeNode) int64 {
	sum := int64(0)
	stack := []*TreeNode{}
	if root != nil {
		stack = append(stack, root)
	}
	for len(stack) > 0 {
		n := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		sum = (sum*31 + n.Val) % 1000000007
		if n.Right != nil {
			stack = append(stack, n.Right)
		}
		if n.Left != nil {
			stack = append(stack, n.Left)
		}
	}
	return sum
}

func main() {
	seed := int64(669)
	order := make([]int64, 10000)
	for i := range order {
		order[i] = int64(i)
	}
	for i := int64(1); i < 10000; i++ {
		j := nextRandom(&seed) % (i + 1)
		order[i], order[j] = order[j], order[i]
	}
	rounds := int64(300)
	sum := int64(0)
	for r := int64(0); r < rounds; r++ {
		low := r * 37 % 10000
		high := low + r*53%5000
		kept := trimBST(bst(order), low, high)
		sum = (sum*31 + checksum(kept)) % 1000000007
	}
	fmt.Printf("10000 nodes, %d rounds: checksum %d\n", rounds, sum)
}
