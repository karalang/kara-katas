// LeetCode #1145: Binary Tree Coloring Game -- the Go mirror of
// btree_game_winning_move.kara: one walk counting every subtree; at the
// first player's node its two sides and the rest of the tree are the
// three parts blue can take, and blue wins when one holds more than half.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func count(node *TreeNode, x int64, sides *[2]int64) int64 {
	if node == nil {
		return 0
	}
	l := count(node.Left, x, sides)
	r := count(node.Right, x, sides)
	if int64(node.Val) == x {
		sides[0], sides[1] = l, r
	}
	return l + r + 1
}

func btreeGameWinningMove(root *TreeNode, n, x int64) bool {
	var sides [2]int64
	count(root, x, &sides)
	l, r := sides[0], sides[1]
	above := n - 1 - l - r
	most := max(l, r, above)
	return most*2 > n
}

var seed int64 = 1145

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(count int64) *TreeNode {
	pool := make([]int32, count)
	for i := range pool {
		pool[i] = int32(i + 1)
	}
	for j := int64(len(pool)) - 1; j >= 1; j-- {
		k := nextRandom() % (j + 1)
		pool[j], pool[k] = pool[k], pool[j]
	}
	nodes := []*TreeNode{{Val: pool[0]}}
	for i := int64(1); i < count; i++ {
		c := &TreeNode{Val: pool[i]}
		for {
			at := nodes[nextRandom()%int64(len(nodes))]
			if nextRandom()%2 == 0 {
				if at.Left == nil {
					at.Left = c
					break
				}
			} else if at.Right == nil {
				at.Right = c
				break
			}
		}
		nodes = append(nodes, c)
	}
	return nodes[0]
}

func main() {
	// 20 trees of 99 nodes, built once. Each of 1000 rounds asks every tree
	// about 99 first moves drawn at random.
	trees := make([]*TreeNode, 20)
	for t := range trees {
		trees[t] = randomTree(99)
	}
	var wins, check int64
	for r := 0; r < 1000; r++ {
		for _, t := range trees {
			for k := 0; k < 99; k++ {
				x := nextRandom()%99 + 1
				answer := btreeGameWinningMove(t, 99, x)
				var a int64
				if answer {
					a = 1
					wins++
				}
				check = (check*31 + x + a) % 1000000007
			}
		}
	}
	fmt.Printf("1000 rounds over 20 trees of 99 nodes: blue wins %d, checksum %d\n", wins, check)
}
