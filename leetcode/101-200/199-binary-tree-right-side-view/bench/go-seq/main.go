package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

func rightView(nodes []Node, root int64) []int64 {
	result := []int64{}
	if root == -1 {
		return result
	}
	level := []int64{root}
	for len(level) > 0 {
		result = append(result, nodes[level[len(level)-1]].val)
		nxt := []int64{}
		for _, idx := range level {
			if nodes[idx].left != -1 {
				nxt = append(nxt, nodes[idx].left)
			}
			if nodes[idx].right != -1 {
				nxt = append(nxt, nodes[idx].right)
			}
		}
		level = nxt
	}
	return result
}

func main() {
	var n int64 = 8191
	var passes int64 = 40000

	nodes := make([]Node, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		v := (state >> 16) % 1000
		li := 2*i + 1
		ri := 2*i + 2
		nodes[i].val = v
		if li < n {
			nodes[i].left = li
		} else {
			nodes[i].left = -1
		}
		if ri < n {
			nodes[i].right = ri
		} else {
			nodes[i].right = -1
		}
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := state % n
		nodes[idx].val = (state >> 16) % 1000
		view := rightView(nodes, 0)
		for _, v := range view {
			sink += v
		}
	}
	fmt.Println(sink)
}
