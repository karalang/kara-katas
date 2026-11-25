// LeetCode #1367 bench -- Go: every tree node tried as the start of the
// list, and from each the list matched down the tree, either child
// carrying the next value.
package main

import "fmt"

type ListNode struct {
	Val  int32
	Next *ListNode
}

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

// the list from `head` on read down from `node`
func matchesFrom(head *ListNode, node *TreeNode) bool {
	if head == nil {
		return true
	}
	if node == nil {
		return false
	}
	return head.Val == node.Val && (matchesFrom(head.Next, node.Left) || matchesFrom(head.Next, node.Right))
}

func isSubPath(head *ListNode, root *TreeNode) bool {
	if root == nil {
		return false
	}
	return matchesFrom(head, root) || isSubPath(head, root.Left) || isSubPath(head, root.Right)
}

var seed int64 = 1367

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type place struct {
	node *TreeNode
	left bool
}

func newNode() *TreeNode {
	return &TreeNode{Val: int32(1 + nextRandom()%2)}
}

func main() {
	// 20 trees of 2500 nodes valued 1 or 2, the constraints' most nodes,
	// each node hung on a random empty child place, built once; then 20000
	// rounds, each flipping one node's value and searching that tree for a
	// list of 8 to 15 values, all drawn from the checksum so far
	trees := make([][]*TreeNode, 20)
	for t := range trees {
		root := newNode()
		nodes := []*TreeNode{root}
		places := []place{{root, true}, {root, false}}
		for i := 1; i < 2500; i++ {
			k := nextRandom() % int64(len(places))
			p := places[k]
			places[k] = places[len(places)-1]
			places = places[:len(places)-1]
			node := newNode()
			if p.left {
				p.node.Left = node
			} else {
				p.node.Right = node
			}
			places = append(places, place{node, true}, place{node, false})
			nodes = append(nodes, node)
		}
		trees[t] = nodes
	}
	var check int64
	hits := 0
	for r := int64(0); r < 20000; r++ {
		nodes := trees[check%20]
		flipped := nodes[(check/20)%2500]
		flipped.Val = 3 - flipped.Val
		m := 8 + check%8
		bits := check / 7
		var head *ListNode
		for k := int64(0); k < m; k++ {
			head = &ListNode{Val: int32(1 + (bits>>k)%2), Next: head}
		}
		found := isSubPath(head, nodes[0])
		if found {
			hits++
		}
		f := int64(0)
		if found {
			f = 1
		}
		check = (check*31 + m*2 + f + r) % 1000000007
	}
	fmt.Printf("20000 rounds over 20 trees of 2500 nodes: %d found, checksum %d\n", hits, check)
}
