package main

import "fmt"

type Node struct {
	val  int64
	next int64
}

func main() {
	var n, cycles int64 = 8000, 7000
	nodes := make([]Node, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		nodes[i].val = state % 50
		nodes[i].next = -1
	}

	var sink int64 = 0
	for c := int64(0); c < cycles; c++ {
		for r := int64(0); r < n; r++ {
			if r+1 < n {
				nodes[r].next = r + 1
			} else {
				nodes[r].next = -1
			}
		}
		for nodes[0].next != -1 {
			var cur int64 = 0
			for cur != -1 && nodes[cur].next != -1 {
				s := nodes[cur].next
				nodes[cur].val = nodes[s].val
				nodes[cur].next = nodes[s].next
				cur = nodes[cur].next
			}
			var pass int64 = 0
			for k := int64(0); k != -1; k = nodes[k].next {
				pass += nodes[k].val
			}
			sink = (sink*31 + pass) & 1073741823
		}
	}
	fmt.Println(sink)
}
