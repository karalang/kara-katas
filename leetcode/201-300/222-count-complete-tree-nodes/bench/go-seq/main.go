package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

func build(n int64) []Node {
	nodes := make([]Node, n)
	for i := int64(0); i < n; i++ {
		l := 2*i + 1
		r := 2*i + 2
		nodes[i].val = i
		if l < n {
			nodes[i].left = l
		} else {
			nodes[i].left = -1
		}
		if r < n {
			nodes[i].right = r
		} else {
			nodes[i].right = -1
		}
	}
	return nodes
}

func leftHeight(nodes []Node, idx int64) int64 {
	var h int64 = 0
	cur := idx
	for cur != -1 {
		h++
		cur = nodes[cur].left
	}
	return h
}

func rightHeight(nodes []Node, idx int64) int64 {
	var h int64 = 0
	cur := idx
	for cur != -1 {
		h++
		cur = nodes[cur].right
	}
	return h
}

func countNodes(nodes []Node, idx int64) int64 {
	if idx == -1 {
		return 0
	}
	lh := leftHeight(nodes, idx)
	rh := rightHeight(nodes, idx)
	if lh == rh {
		return (int64(1) << lh) - 1
	}
	return 1 + countNodes(nodes, nodes[idx].left) + countNodes(nodes, nodes[idx].right)
}

func main() {
	var n int64 = 2000000
	var passes int64 = 2000000
	var topSpan int64 = 2048
	var modulus int64 = 1000000007

	nodes := build(n)

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		start := p % topSpan
		sink = (sink + countNodes(nodes, start)) % modulus
	}
	fmt.Println(sink)
}
