// Benchmark: LeetCode #1080 Insufficient Nodes in Root to Leaf Paths --
// the ★ arm. Mirrors ../sufficient_subset.kara, .rs, .c and .py.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func prune(n *TreeNode, need int64) *TreeNode {
	if n == nil {
		return nil
	}
	if n.Left == nil && n.Right == nil {
		if int64(n.Val) >= need {
			return n
		}
		return nil
	}
	n.Left = prune(n.Left, need-int64(n.Val))
	n.Right = prune(n.Right, need-int64(n.Val))
	if n.Left == nil && n.Right == nil {
		return nil
	}
	return n
}

func sufficientSubset(root *TreeNode, limit int64) *TreeNode { return prune(root, limit) }

var seed int64 = 1080

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type shape struct {
	val         []int32
	left, right []int64
}

func randomShape(n int64) shape {
	var s shape
	for k := int64(0); k < n; k++ {
		s.val = append(s.val, int32(nextRandom()%201-100))
		s.left = append(s.left, -1)
		s.right = append(s.right, -1)
		if k > 0 {
			at := int64(0)
			for {
				if nextRandom()%2 == 0 {
					if s.left[at] < 0 {
						s.left[at] = k
						break
					}
					at = s.left[at]
				} else {
					if s.right[at] < 0 {
						s.right[at] = k
						break
					}
					at = s.right[at]
				}
			}
		}
	}
	return s
}

func build(s *shape, k int64) *TreeNode {
	if k < 0 {
		return nil
	}
	return &TreeNode{Val: s.val[k], Left: build(s, s.left[k]), Right: build(s, s.right[k])}
}

func count(t *TreeNode) int64 {
	if t == nil {
		return 0
	}
	return 1 + count(t.Left) + count(t.Right)
}

func main() {
	rounds := int64(100)
	shapes := make([]shape, 200)
	for i := range shapes {
		shapes[i] = randomShape(1000)
	}
	var kept, check int64
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < 200; i++ {
			limit := (r*37+i*11)%401 - 200
			k := count(sufficientSubset(build(&shapes[i], 0), limit))
			kept += k
			check = (check*31 + k + i) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 200 trees of 1000 nodes: %d nodes kept, checksum %d\n", rounds, kept, check)
}
