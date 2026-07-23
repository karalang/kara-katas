package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

var nodes []Node

func insert(root int64, v int64) int64 {
	if root == -1 {
		idx := int64(len(nodes))
		nodes = append(nodes, Node{val: v, left: -1, right: -1})
		return idx
	}
	if v < nodes[root].val {
		l := insert(nodes[root].left, v)
		nodes[root].left = l
	} else {
		r := insert(nodes[root].right, v)
		nodes[root].right = r
	}
	return root
}

func kthSmallest(root int64, k int64) int64 {
	stack := make([]int64, 0)
	cur := root
	var count int64 = 0
	for cur != -1 || len(stack) > 0 {
		for cur != -1 {
			stack = append(stack, cur)
			cur = nodes[cur].left
		}
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		count += 1
		if count == k {
			return nodes[node].val
		}
		cur = nodes[node].right
	}
	return -1
}

func main() {
	var n int64 = 3000
	var queries int64 = 140000

	nodes = make([]Node, 0, n)
	var root int64 = -1
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		root = insert(root, state)
	}

	var sink int64 = 0
	for q := int64(0); q < queries; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		k := 1 + (state % n)
		sink += kthSmallest(root, k)
	}
	fmt.Println(sink)
}
