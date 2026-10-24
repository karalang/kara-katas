// Benchmark: LeetCode #979 Distribute Coins in Binary Tree -- the ★ arm,
// excess from the leaves, on random trees of 100 nodes, LeetCode's
// largest. Mirrors distribute_coins.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func excess(t *TreeNode, moves *int64) int64 {
	if t == nil {
		return 0
	}
	l := excess(t.Left, moves)
	r := excess(t.Right, moves)
	*moves += abs(l) + abs(r)
	return t.Val + l + r - 1
}

func distributeCoins(root *TreeNode) int64 {
	var moves int64
	excess(root, &moves)
	return moves
}

var seed int64 = 979

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	nodes := []*TreeNode{{}}
	for i := 1; i < n; i++ {
		node := &TreeNode{}
		cur := nodes[0]
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
		nodes = append(nodes, node)
	}
	for i := 0; i < n; i++ {
		nodes[nextRandom()%int64(n)].Val++
	}
	return nodes[0]
}

func main() {
	rounds := 200
	trees := make([]*TreeNode, 2000)
	for i := range trees {
		trees[i] = randomTree(100)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 2000; i++ {
			m := distributeCoins(trees[(r+i)%2000])
			total += m
			check = (check*31 + m + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 2000 trees of 100 nodes: %d moves, checksum %d\n", rounds, total, check)
}
