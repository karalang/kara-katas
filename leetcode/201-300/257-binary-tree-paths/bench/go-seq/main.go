// Benchmark workload for LeetCode #257 — Binary Tree Paths (Go mirror).
// Mirrors binary_tree_paths.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"strconv"
)

type Node struct{ val, left, right int64 }

var nodes []Node
var out []string

func walk(node int64, prefix string) {
	left, right := nodes[node].left, nodes[node].right
	if left == -1 && right == -1 {
		out = append(out, prefix)
		return
	}
	if left != -1 {
		walk(left, prefix+"->"+strconv.FormatInt(nodes[left].val, 10))
	}
	if right != -1 {
		walk(right, prefix+"->"+strconv.FormatInt(nodes[right].val, 10))
	}
}

func main() {
	var n int64 = 150000
	var rounds int64 = 5

	nodes = make([]Node, 0, n)
	open := make([]int64, 0, n)
	var state int64 = 257257

	state = (state*1103515245 + 12345) & 2147483647
	nodes = append(nodes, Node{(state / 65536) % 100 % 100 - 50, -1, -1})
	open = append(open, 0)

	for int64(len(nodes)) < n {
		state = (state*1103515245 + 12345) & 2147483647
		wd0 := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		pick := (wd0 * 32768 + state / 65536) % int64(len(open))
		parent := open[pick]
		state = (state*1103515245 + 12345) & 2147483647
		nodes = append(nodes, Node{(state / 65536) % 100 % 100 - 50, -1, -1})
		child := int64(len(nodes)) - 1
		if nodes[parent].left == -1 {
			nodes[parent].left = child
		} else {
			nodes[parent].right = child
			open[pick] = open[len(open)-1]
			open = open[:len(open)-1]
		}
		open = append(open, child)
	}

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		out = out[:0]
		walk(0, strconv.FormatInt(nodes[0].val, 10))

		var h int64 = 1
		for _, s := range out {
			for _, b := range []byte(s) {
				h = (h*1000003 + int64(b)) % 1000000007
			}
			h = (h*31 + 7) % 1000000007
		}
		sink = (sink*131 + h) % 1000000007
	}
	fmt.Println(sink)
}
