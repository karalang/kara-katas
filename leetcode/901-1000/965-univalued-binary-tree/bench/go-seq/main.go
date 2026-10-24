// Benchmark: LeetCode #965 Univalued Binary Tree -- the ★ arm, depth
// first, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_unival_tree.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func holds(t *TreeNode, v int64) bool {
	if t == nil {
		return true
	}
	return t.Val == v && holds(t.Left, v) && holds(t.Right, v)
}

func isUnivalTree(root *TreeNode) bool {
	if root == nil {
		return true
	}
	return holds(root.Left, root.Val) && holds(root.Right, root.Val)
}

var seed int64 = 965

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func attach(root, node *TreeNode) {
	cur := root
	for {
		if nextRandom()%2 == 0 {
			if cur.Left != nil {
				cur = cur.Left
			} else {
				cur.Left = node
				return
			}
		} else {
			if cur.Right != nil {
				cur = cur.Right
			} else {
				cur.Right = node
				return
			}
		}
	}
}

func makeTree(kind, n int) *TreeNode {
	v := nextRandom() % 100
	vals := make([]int64, n)
	for i := range vals {
		vals[i] = v
	}
	if kind == 3 {
		for i := range vals {
			vals[i] = nextRandom() % 2
		}
	} else {
		for j := 0; j < kind; j++ {
			k := int(nextRandom()) % n
			vals[k] = nextRandom() % 100
		}
	}
	root := &TreeNode{Val: vals[0]}
	for _, val := range vals[1:] {
		attach(root, &TreeNode{Val: val})
	}
	return root
}

func main() {
	rounds := 4000
	trees := make([]*TreeNode, 200)
	for i := range trees {
		trees[i] = makeTree(i%4, 100)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 200; i++ {
			var bit int64
			if isUnivalTree(trees[(r+i)%200]) {
				bit = 1
			}
			total += bit
			check = (check*31 + bit + 1 + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 200 trees of 100 nodes: %d univalued, checksum %d\n", rounds, total, check)
}
