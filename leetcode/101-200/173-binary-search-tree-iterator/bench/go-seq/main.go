package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

var nodes []Node

func insert(root, val int64) int64 {
	if root == -1 {
		nodes = append(nodes, Node{val: val, left: -1, right: -1})
		return int64(len(nodes)) - 1
	}
	if val < nodes[root].val {
		li := nodes[root].left
		nodes[root].left = insert(li, val)
	} else {
		ri := nodes[root].right
		nodes[root].right = insert(ri, val)
	}
	return root
}

func main() {
	var n, passes int64 = 4000, 30000
	nodes = make([]Node, 0, n)
	var root int64 = -1
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		v := state % 1000
		root = insert(root, v)
	}

	stack := make([]int64, 0, n)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*1315423911 + 7) % n
		nodes[idx].val = (nodes[idx].val + 1) % 1000

		stack = stack[:0]
		cur := root
		for cur != -1 {
			stack = append(stack, cur)
			cur = nodes[cur].left
		}
		var pos int64 = 1
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			sink += pos * nodes[top].val
			pos++
			r := nodes[top].right
			for r != -1 {
				stack = append(stack, r)
				r = nodes[r].left
			}
		}
	}
	fmt.Println(sink)
}
