// Benchmark for #654: a stack of the right spine, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func constructMaximumBinaryTree(nums []int64) *TreeNode {
	stack := []*TreeNode{}
	for _, x := range nums {
		node := &TreeNode{val: x}
		for len(stack) > 0 && stack[len(stack)-1].val < x {
			node.left = stack[len(stack)-1]
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			stack[len(stack)-1].right = node
		}
		stack = append(stack, node)
	}
	if len(stack) == 0 {
		return nil
	}
	return stack[0]
}

var seed int64 = 654

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	inputs, rounds := 8, 100
	var n int64 = 200000
	lists := [][]int64{}
	for k := 0; k < inputs; k++ {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i)
		}
		for i := n - 1; i > 0; i-- {
			hi := nextRandom()
			j := (hi*32768 + nextRandom()) % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		lists = append(lists, nums)
	}
	var checksum int64
	for r := 0; r < rounds; r++ {
		root := constructMaximumBinaryTree(lists[(r*3)%inputs])
		var left, right int64
		for at := root; at != nil; at = at.left {
			left++
		}
		for at := root; at != nil; at = at.right {
			right++
		}
		checksum = (checksum*31 + left*1000 + right) % 1000000007
	}
	fmt.Printf("%d orders of %d, %d rounds: checksum %d\n", inputs, n, rounds, checksum)
}
