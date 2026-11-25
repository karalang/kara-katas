// LeetCode #1379 bench -- Go: the ★ arm: the two trees walked together,
// depth first; the clone's node where the original's is the target itself
// (the same pointer) is the answer.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func find(o, c, target *TreeNode) *TreeNode {
	if o == target {
		return c
	}
	if o.Left != nil && c.Left != nil {
		if found := find(o.Left, c.Left, target); found != nil {
			return found
		}
	}
	if o.Right != nil && c.Right != nil {
		return find(o.Right, c.Right, target)
	}
	return nil
}

func getTargetCopy(original, cloned, target *TreeNode) *TreeNode {
	return find(original, cloned, target)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func cloneTree(node *TreeNode) *TreeNode {
	copy := &TreeNode{Val: node.Val}
	if node.Left != nil {
		copy.Left = cloneTree(node.Left)
	}
	if node.Right != nil {
		copy.Right = cloneTree(node.Right)
	}
	return copy
}

type place struct {
	node *TreeNode
	left bool
}

func main() {
	// 10 trees of 10^4 nodes built once, with their clones; then 3000
	// rounds, each asking one tree's clone for the copy of one node (see
	// the Kāra bench)
	const n = int64(10000)
	seed := int64(1379)
	var originals, clones [10]*TreeNode
	var nodes [10][]*TreeNode
	for t := 0; t < 10; t++ {
		root := &TreeNode{Val: 1}
		nodes[t] = []*TreeNode{root}
		open := []place{{root, true}, {root, false}}
		for k := int64(1); k < n; k++ {
			at := nextRandom(&seed) % int64(len(open))
			p := open[at]
			open[at] = open[len(open)-1]
			open = open[:len(open)-1]
			node := &TreeNode{Val: int32(k + 1)}
			if p.left {
				p.node.Left = node
			} else {
				p.node.Right = node
			}
			open = append(open, place{node, true}, place{node, false})
			nodes[t] = append(nodes[t], node)
		}
		originals[t] = root
		clones[t] = cloneTree(root)
	}
	check := int64(0)
	for r := int64(0); r < 3000; r++ {
		t := check % 10
		target := nodes[t][(check/10+r)%n]
		found := getTargetCopy(originals[t], clones[t], target)
		own := int64(1)
		if found == target {
			own = 0
		}
		check = (check*31 + int64(found.Val)*2 + own + r) % 1000000007
	}
	fmt.Printf("3000 rounds over 10 trees of 10000 nodes: checksum %d\n", check)
}
