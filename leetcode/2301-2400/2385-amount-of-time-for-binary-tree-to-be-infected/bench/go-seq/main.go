// LeetCode #2385: Amount of Time for Binary Tree to Be Infected -- the
// bench, the ★ arm in Go: one post-order walk returning each subtree's
// height and the start's distance below it. The nodes are `*TreeNode`.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func walk(node *TreeNode, start int64, best *int64) (int64, int64) {
	if node == nil {
		return 0, -1
	}
	lh, ld := walk(node.Left, start, best)
	rh, rd := walk(node.Right, start, best)
	height := 1 + max(lh, rh)
	if int64(node.Val) == start {
		*best = max(*best, max(lh, rh))
		return height, 0
	}
	if ld >= 0 {
		*best = max(*best, ld+1+rh)
		return height, ld + 1
	}
	if rd >= 0 {
		*best = max(*best, rd+1+lh)
		return height, rd + 1
	}
	return height, -1
}

func amountOfTime(root *TreeNode, start int64) int64 {
	best := int64(0)
	walk(root, start, &best)
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2385

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i + 1)
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % int64(i+1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*TreeNode, n)
	for i := range nodes {
		nodes[i] = &TreeNode{Val: values[i]}
	}
	for k := 1; k < n; k++ {
		high := nextRandom()
		at := nodes[(high*32768+nextRandom())%int64(k)]
		for {
			if nextRandom()%2 == 0 {
				if at.Left != nil {
					at = at.Left
				} else {
					at.Left = nodes[k]
					break
				}
			} else {
				if at.Right != nil {
					at = at.Right
				} else {
					at.Right = nodes[k]
					break
				}
			}
		}
	}
	return nodes[0]
}

func main() {
	// 200 random trees of 1000 nodes, each asked from 400 starts, start s
	// of tree t being 1 + (37 s + t) % 1000
	check := int64(0)
	for t := int64(0); t < 200; t++ {
		root := randomTree(1000)
		for s := int64(0); s < 400; s++ {
			check = (check*31 + amountOfTime(root, 1+(37*s+t)%1000)) % 1000000007
		}
	}
	fmt.Printf("200 trees of 1000, 400 starts each: checksum %d\n", check)
}
