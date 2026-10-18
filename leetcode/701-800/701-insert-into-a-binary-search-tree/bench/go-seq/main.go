// LeetCode #701: Insert into a Binary Search Tree -- bench program, Go mirror of the loop arm.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func insertIntoBST(root *TreeNode, val int64) *TreeNode {
	fresh := &TreeNode{val: val}
	if root == nil {
		return fresh
	}
	at := root
	for {
		if val < at.val {
			if at.left != nil {
				at = at.left
			} else {
				at.left = fresh
				return root
			}
		} else {
			if at.right != nil {
				at = at.right
			} else {
				at.right = fresh
				return root
			}
		}
	}
}

type frame struct {
	node  *TreeNode
	depth int64
}

func height(root *TreeNode) int64 {
	best := int64(0)
	var stack []frame
	if root != nil {
		stack = append(stack, frame{root, 1})
	}
	for len(stack) > 0 {
		f := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if f.depth > best {
			best = f.depth
		}
		if f.node.right != nil {
			stack = append(stack, frame{f.node.right, f.depth + 1})
		}
		if f.node.left != nil {
			stack = append(stack, frame{f.node.left, f.depth + 1})
		}
	}
	return best
}

func main() {
	seed := int64(701)
	const n = int64(50000)
	orders := make([][]int64, 0, 10)
	for t := 0; t < 10; t++ {
		values := make([]int64, n)
		for i := int64(0); i < n; i++ {
			values[i] = 2 * i
		}
		for i := int64(1); i < n; i++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			j := (hi*32768 + lo) % (i + 1)
			values[i], values[j] = values[j], values[i]
		}
		orders = append(orders, values)
	}
	const rounds = 5
	total := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for _, order := range orders {
			var root *TreeNode
			for _, v := range order {
				root = insertIntoBST(root, v)
			}
			h := height(root)
			total += h
			checksum = (checksum*31 + h) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 10 trees grown to %d: heights sum to %d, checksum %d\n", rounds, n, total, checksum)
}
