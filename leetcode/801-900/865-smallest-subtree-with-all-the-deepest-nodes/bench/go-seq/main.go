// LeetCode #865: Smallest Subtree with all the Deepest Nodes -- Go mirror
// of the bench program (the ★ arm, one recursive pass).
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func subtreeWithAllDeepest(root *TreeNode) *TreeNode {
	_, found := deepest(root)
	return found
}

func deepest(node *TreeNode) (int64, *TreeNode) {
	if node == nil {
		return 0, nil
	}
	dl, l := deepest(node.Left)
	dr, r := deepest(node.Right)
	if dl == dr {
		return dl + 1, node
	}
	if dl > dr {
		return dl + 1, l
	}
	return dr + 1, r
}

var seed int64 = 865

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int64) *TreeNode {
	vals := make([]int64, n)
	for v := range vals {
		vals[v] = int64(v)
	}
	for i := int64(1); i < n; i++ {
		j := nextRandom() % (i + 1)
		vals[i], vals[j] = vals[j], vals[i]
	}
	var nodes []*TreeNode
	for k := int64(0); k < n; k++ {
		node := &TreeNode{Val: vals[k]}
		if k > 0 {
			for {
				parent := nodes[nextRandom()%int64(len(nodes))]
				if nextRandom()%2 == 0 {
					if parent.Left == nil {
						parent.Left = node
						break
					}
				} else if parent.Right == nil {
					parent.Right = node
					break
				}
			}
		}
		nodes = append(nodes, node)
	}
	if n == 0 {
		return nil
	}
	return nodes[0]
}

func main() {
	n, rounds := int64(500), 300000
	root := randomTree(n)
	var nodes []*TreeNode
	stack := []*TreeNode{root}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if node.Left != nil {
			stack = append(stack, node.Left)
		}
		if node.Right != nil {
			stack = append(stack, node.Right)
		}
		nodes = append(nodes, node)
	}
	leaf := &TreeNode{Val: n}
	var total, check int64
	for q := 0; q < rounds; q++ {
		at := nodes[nextRandom()%n]
		for at.Left != nil && at.Right != nil {
			at = nodes[nextRandom()%n]
		}
		onLeft := at.Left == nil
		if onLeft {
			at.Left = leaf
		} else {
			at.Right = leaf
		}
		found := int64(-1)
		if f := subtreeWithAllDeepest(root); f != nil {
			found = f.Val
		}
		if onLeft {
			at.Left = nil
		} else {
			at.Right = nil
		}
		total += found
		check = (check*31 + found + 1) % 1000000007
	}
	fmt.Printf("%d rounds on %d nodes: answers sum to %d, checksum %d\n", rounds, n, total, check)
}
