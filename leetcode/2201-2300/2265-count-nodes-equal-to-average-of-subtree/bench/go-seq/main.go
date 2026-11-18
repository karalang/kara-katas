// LeetCode #2265: Count Nodes Equal to Average of Subtree -- Go mirror of
// the ★ arm (average.kara): the same random trees of `*TreeNode`, each
// counted by one post-order walk returning the sum and the size. Output
// is byte-identical to average.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func sumAndSize(node *TreeNode, matches *int64) (int64, int64) {
	if node == nil {
		return 0, 0
	}
	ls, lc := sumAndSize(node.Left, matches)
	rs, rc := sumAndSize(node.Right, matches)
	sum := ls + rs + int64(node.Val)
	size := lc + rc + 1
	if sum/size == int64(node.Val) {
		*matches++
	}
	return sum, size
}

func averageOfSubtree(root *TreeNode) int64 {
	var matches int64
	sumAndSize(root, &matches)
	return matches
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2265

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int, top int64) *TreeNode {
	nodes := make([]*TreeNode, n)
	for i := range nodes {
		nodes[i] = &TreeNode{Val: int32(nextRandom() % (top + 1))}
	}
	for k := 1; k < n; k++ {
		at := nodes[nextRandom()%int64(k)]
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
	var check int64
	for t := 0; t < 500; t++ {
		root := randomTree(1000, 1000)
		for r := 0; r < 20; r++ {
			check = (check*31 + averageOfSubtree(root)) % 1000000007
		}
	}
	fmt.Printf("500 trees of 1000, 20 times: checksum %d\n", check)
}
