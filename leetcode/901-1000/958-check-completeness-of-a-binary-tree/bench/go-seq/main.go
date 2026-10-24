// Benchmark: LeetCode #958 Check Completeness of a Binary Tree -- the ★
// arm, the first gap, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_complete_tree.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func isCompleteTree(root *TreeNode) bool {
	queue := []*TreeNode{root}
	gap := false
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if node == nil {
			gap = true
		} else {
			if gap {
				return false
			}
			queue = append(queue, node.Left, node.Right)
		}
	}
	return true
}

var seed int64 = 958

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func newNode() *TreeNode {
	return &TreeNode{Val: 1 + nextRandom()%1000}
}

// Node i of the complete tree is a left child (side 0) when i is odd.
func sideOf(i int) int { return (i + 1) % 2 }

func setChild(parent *TreeNode, side int, child *TreeNode) {
	if side == 0 {
		parent.Left = child
	} else {
		parent.Right = child
	}
}

func completeTree(n int) []*TreeNode {
	nodes := make([]*TreeNode, n)
	for i := range nodes {
		nodes[i] = newNode()
	}
	for i := 1; i < n; i++ {
		setChild(nodes[(i-1)/2], sideOf(i), nodes[i])
	}
	return nodes
}

func randomTree(n int) *TreeNode {
	root := newNode()
	for i := 1; i < n; i++ {
		node := newNode()
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

func makeTree(kind, n int) *TreeNode {
	if kind == 3 {
		return randomTree(n)
	}
	// nodes is the level order of the complete tree
	nodes := completeTree(n)
	if n < 2 {
		return nodes[0]
	}
	switch kind {
	case 1:
		last := nodes[n-1]
		setChild(nodes[(n-2)/2], sideOf(n-1), nil)
		var parents []*TreeNode
		var sides []int
		for _, node := range nodes[:n-1] {
			if node.Left == nil {
				parents = append(parents, node)
				sides = append(sides, 0)
			}
			if node.Right == nil {
				parents = append(parents, node)
				sides = append(sides, 1)
			}
		}
		k := int(nextRandom()) % len(parents)
		setChild(parents[k], sides[k], last)
	case 2:
		var leaves []int
		for i := 1; i < n; i++ {
			if nodes[i].Left == nil && nodes[i].Right == nil {
				leaves = append(leaves, i)
			}
		}
		i := leaves[int(nextRandom())%len(leaves)]
		setChild(nodes[(i-1)/2], sideOf(i), nil)
	case 4:
		node := nodes[int(nextRandom())%n]
		node.Left, node.Right = node.Right, node.Left
	}
	return nodes[0]
}

func main() {
	rounds := 4000
	trees := make([]*TreeNode, 200)
	for i := range trees {
		trees[i] = makeTree(i%5, 100)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 200; i++ {
			var bit int64
			if isCompleteTree(trees[(r+i)%200]) {
				bit = 1
			}
			total += bit
			check = (check*31 + bit + 1 + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 200 trees of up to 100 nodes: %d complete, checksum %d\n", rounds, total, check)
}
