// LeetCode #1110: Delete Nodes And Return Forest -- the bench in Go: the
// ★ arm over the same 16 trees of 1000 nodes and the same rounds, the
// nodes on Go's collected heap and the values to delete in a built-in map.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func prune(node *TreeNode, parentGone bool, gone map[int32]bool, roots *[]*TreeNode) *TreeNode {
	if node == nil {
		return nil
	}
	deleted := gone[node.Val]
	if parentGone && !deleted {
		*roots = append(*roots, node)
	}
	node.Left = prune(node.Left, deleted, gone, roots)
	node.Right = prune(node.Right, deleted, gone, roots)
	if deleted {
		return nil
	}
	return node
}

func delNodes(root *TreeNode, toDelete []int32) []*TreeNode {
	gone := make(map[int32]bool)
	for _, v := range toDelete {
		gone[v] = true
	}
	roots := []*TreeNode{}
	prune(root, true, gone, &roots)
	return roots
}

var seed int64 = 1110

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type Shape struct {
	values      []int32
	left, right []int64
}

func shape() Shape {
	values := make([]int32, 1000)
	for i := range values {
		values[i] = int32(i + 1)
	}
	for i := int64(0); i < 1000; i++ {
		j := i + nextRandom()%(1000-i)
		values[i], values[j] = values[j], values[i]
	}
	left := make([]int64, 1000)
	right := make([]int64, 1000)
	for i := range left {
		left[i] = -1
		right[i] = -1
	}
	for k := int64(1); k < 1000; k++ {
		for {
			at := nextRandom() % k
			if nextRandom()%2 == 0 {
				if left[at] < 0 {
					left[at] = k
					break
				}
			} else if right[at] < 0 {
				right[at] = k
				break
			}
		}
	}
	return Shape{values, left, right}
}

func build(s *Shape) *TreeNode {
	nodes := make([]*TreeNode, 1000)
	for k, v := range s.values {
		nodes[k] = &TreeNode{Val: v}
	}
	for k := 0; k < 1000; k++ {
		if s.left[k] >= 0 {
			nodes[k].Left = nodes[s.left[k]]
		}
		if s.right[k] >= 0 {
			nodes[k].Right = nodes[s.right[k]]
		}
	}
	return nodes[0]
}

func main() {
	shapes := make([]Shape, 16)
	for i := range shapes {
		shapes[i] = shape()
	}
	trees := 0
	var check int64
	for round := 0; round < 200; round++ {
		for j := range shapes {
			third := int32((round + j) % 3)
			toDelete := []int32{}
			for v := int32(1); v <= 1000; v++ {
				if v%3 == third {
					toDelete = append(toDelete, v)
				}
			}
			roots := delNodes(build(&shapes[j]), toDelete)
			trees += len(roots)
			for _, r := range roots {
				check = (check*31 + int64(r.Val)) % 1000000007
			}
		}
	}
	fmt.Printf("200 rounds over 16 trees of 1000 nodes: %d trees, checksum %d\n", trees, check)
}
