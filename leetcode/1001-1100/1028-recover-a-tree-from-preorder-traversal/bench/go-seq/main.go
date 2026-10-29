// LeetCode #1028: Recover a Tree From Preorder Traversal -- bench
// Mirrors ../recover_tree.kara; see ../../README.md § Benchmarks.

package main

import (
	"fmt"
	"strconv"
	"strings"
)

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func recoverFromPreorder(traversal string) *TreeNode {
	path := []*TreeNode{}
	i := 0
	for i < len(traversal) {
		depth := 0
		for traversal[i] == '-' {
			depth++
			i++
		}
		value := int64(0)
		for i < len(traversal) && traversal[i] != '-' {
			value = value*10 + int64(traversal[i]-'0')
			i++
		}
		node := &TreeNode{Val: value}
		if len(path) > depth {
			path = path[:depth]
		}
		if len(path) > 0 {
			parent := path[len(path)-1]
			if parent.Left == nil {
				parent.Left = node
			} else {
				parent.Right = node
			}
		}
		path = append(path, node)
	}
	if len(path) > 0 {
		return path[0]
	}
	return nil
}

// a fold of the tree's values and shape
func digest(node *TreeNode) int64 {
	if node == nil {
		return 1
	}
	return (node.Val + 3*digest(node.Left) + 7*digest(node.Right)) % 1000000007
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64, top int64) int64 {
	a := nextRandom(seed)
	b := nextRandom(seed)
	return (a*32768+b)%top + 1
}

func write(at, depth int64, vals, left, right []int64, out *strings.Builder) {
	for d := int64(0); d < depth; d++ {
		out.WriteByte('-')
	}
	out.WriteString(strconv.FormatInt(vals[at], 10))
	if left[at] >= 0 {
		write(left[at], depth+1, vals, left, right, out)
	}
	if right[at] >= 0 {
		write(right[at], depth+1, vals, left, right, out)
	}
}

func makeTraversal(seed *int64, n int64) string {
	vals := []int64{}
	left := []int64{}
	right := []int64{}
	for k := int64(0); k < n; k++ {
		v := randomValue(seed, 1000000000)
		vals = append(vals, v)
		left = append(left, -1)
		right = append(right, -1)
		at := int64(0)
		for k > 0 {
			if v < vals[at] {
				if left[at] < 0 {
					left[at] = k
					break
				}
				at = left[at]
			} else {
				if right[at] < 0 {
					right[at] = k
					break
				}
				at = right[at]
			}
		}
	}
	var out strings.Builder
	write(0, 0, vals, left, right, &out)
	return out.String()
}

func main() {
	const count, rounds = 200, 50
	seed := int64(1028)
	traversals := []string{}
	letters := 0
	for k := 0; k < count; k++ {
		s := makeTraversal(&seed, 1000)
		letters += len(s)
		traversals = append(traversals, s)
	}
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, s := range traversals {
			check = (check*131 + digest(recoverFromPreorder(s))) % 1000000007
		}
	}
	fmt.Printf("%d traversals of 1000 nodes, %d letters, %d rounds: checksum %d\n", count, letters, rounds, check)
}
