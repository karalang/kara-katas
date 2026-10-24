// Benchmark: LeetCode #968 Binary Tree Cameras -- the ★ arm, greedy from
// the leaves, on random trees of 1000 nodes, LeetCode's largest. Mirrors
// min_camera_cover.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

// 0 not yet covered, 1 holds a camera, 2 covered without one.
func watch(t *TreeNode, cameras *int64) int {
	if t == nil {
		return 2
	}
	l := watch(t.Left, cameras)
	r := watch(t.Right, cameras)
	if l == 0 || r == 0 {
		*cameras++
		return 1
	}
	if l == 1 || r == 1 {
		return 2
	}
	return 0
}

func minCameraCover(root *TreeNode) int64 {
	var cameras int64
	if watch(root, &cameras) == 0 {
		cameras++
	}
	return cameras
}

var seed int64 = 968

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	root := &TreeNode{}
	for i := 1; i < n; i++ {
		node := &TreeNode{}
		cur := root
		for {
			if nextRandom()%2 == 0 {
				if cur.Left != nil {
					cur = cur.Left
				} else {
					cur.Left = node
					break
				}
			} else {
				if cur.Right != nil {
					cur = cur.Right
				} else {
					cur.Right = node
					break
				}
			}
		}
	}
	return root
}

func main() {
	rounds := 200
	trees := make([]*TreeNode, 200)
	for i := range trees {
		trees[i] = randomTree(1000)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 200; i++ {
			c := minCameraCover(trees[(r+i)%200])
			total += c
			check = (check*31 + c + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 200 trees of 1000 nodes: %d cameras, checksum %d\n", rounds, total, check)
}
