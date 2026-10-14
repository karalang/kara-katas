// Benchmark for #572: Go mirror of the ★ arm (recursion); see
// is_subtree.kara.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func sameTree(a, b *TreeNode) bool {
	if a == nil && b == nil {
		return true
	}
	if a != nil && b != nil {
		return a.Val == b.Val && sameTree(a.Left, b.Left) && sameTree(a.Right, b.Right)
	}
	return false
}

func isSubtree(root, subRoot *TreeNode) bool {
	if sameTree(root, subRoot) {
		return true
	}
	if root == nil {
		return false
	}
	return isSubtree(root.Left, subRoot) || isSubtree(root.Right, subRoot)
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomTree(size int64, seed *int64) *TreeNode {
	root := &TreeNode{Val: nextRandom(seed) % 2}
	for i := int64(1); i < size; i++ {
		c := &TreeNode{Val: nextRandom(seed) % 2}
		node := root
		for {
			if nextRandom(seed)%2 == 0 {
				if node.Left != nil {
					node = node.Left
				} else {
					node.Left = c
					break
				}
			} else {
				if node.Right != nil {
					node = node.Right
				} else {
					node.Right = c
					break
				}
			}
		}
	}
	return root
}

func copyTree(node *TreeNode) *TreeNode {
	if node == nil {
		return nil
	}
	return &TreeNode{Val: node.Val, Left: copyTree(node.Left), Right: copyTree(node.Right)}
}

func allNodes(node *TreeNode, out []*TreeNode) []*TreeNode {
	if node != nil {
		out = append(out, node)
		out = allNodes(node.Left, out)
		out = allNodes(node.Right, out)
	}
	return out
}

func main() {
	var count int64 = 20
	var rounds int64 = 1000
	var seed int64 = 572
	roots := make([]*TreeNode, 0, count)
	subs := make([]*TreeNode, 0, count)
	for g := int64(0); g < count; g++ {
		root := randomTree(2000, &seed)
		nodes := allNodes(root, nil)
		var picked *TreeNode
		for {
			picked = nodes[nextRandom(&seed)%int64(len(nodes))]
			if len(allNodes(picked, nil)) >= 20 {
				break
			}
		}
		sub := copyTree(picked)
		if g%2 == 1 {
			inside := allNodes(sub, nil)
			n := inside[nextRandom(&seed)%int64(len(inside))]
			n.Val = 1 - n.Val
		}
		roots = append(roots, root)
		subs = append(subs, sub)
	}
	var found int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := isSubtree(roots[p], subs[p])
			add := int64(1)
			if got {
				found += 1
				add = g + 2
			}
			checksum = (checksum*31 + add) % 1000000007
		}
	}
	fmt.Printf("%d pairs, %d rounds: %d found, checksum %d\n", count, rounds, found, checksum)
}
