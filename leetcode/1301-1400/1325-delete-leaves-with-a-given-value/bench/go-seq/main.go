// LeetCode #1325 bench in Go: the ★ arm (a recursive walk that settles both
// children first and deletes a leaf with the target's value) on the same 30
// trees of 3000 nodes and 300 passes, each linking every node back to its
// children first.
package main

import "fmt"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func removeLeafNodes(node *TreeNode, target int) *TreeNode {
	if node == nil {
		return nil
	}
	node.Left = removeLeafNodes(node.Left, target)
	node.Right = removeLeafNodes(node.Right, target)
	if node.Left == nil && node.Right == nil && node.Val == target {
		return nil
	}
	return node
}

func count(node *TreeNode) int64 {
	if node == nil {
		return 0
	}
	return 1 + count(node.Left) + count(node.Right)
}

var seed int64 = 1325

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type place struct {
	parent int64
	isLeft bool
}

type Tree struct {
	nodes []*TreeNode
	left  []int64
	right []int64
}

func build(n int64, deep bool) Tree {
	t := Tree{}
	places := []place{{0, true}, {0, false}}
	for i := int64(0); i < n; i++ {
		t.nodes = append(t.nodes, &TreeNode{Val: int(1 + nextRandom()%3)})
		t.left = append(t.left, -1)
		t.right = append(t.right, -1)
		if i > 0 {
			r := nextRandom()
			var at int64
			if deep && r%4 != 0 {
				at = int64(len(places)) - 1 - nextRandom()%2
			} else {
				at = nextRandom() % int64(len(places))
			}
			p := places[at]
			places[at] = places[len(places)-1]
			places = places[:len(places)-1]
			if p.isLeft {
				t.left[p.parent] = i
			} else {
				t.right[p.parent] = i
			}
			places = append(places, place{i, true}, place{i, false})
		}
	}
	return t
}

func main() {
	const n = 3000
	trees := make([]Tree, 0, 30)
	for t := 0; t < 30; t++ {
		trees = append(trees, build(n, t%2 == 1))
	}
	var check int64
	for pass := int64(0); pass < 300; pass++ {
		for t := 0; t < 30; t++ {
			tree := &trees[t]
			tree.nodes[check%n].Val = int(1 + (check/7)%3)
			target := int(1 + (check/11)%3)
			for i := 0; i < n; i++ {
				node := tree.nodes[i]
				node.Left = nil
				node.Right = nil
				if tree.left[i] >= 0 {
					node.Left = tree.nodes[tree.left[i]]
				}
				if tree.right[i] >= 0 {
					node.Right = tree.nodes[tree.right[i]]
				}
			}
			root := removeLeafNodes(tree.nodes[0], target)
			var top int64
			if root != nil {
				top = int64(root.Val)
			}
			check = (check*31 + count(root)*7 + top + pass) % 1000000007
		}
	}
	fmt.Printf("300 passes over 30 trees of 3000: checksum %d\n", check)
}
