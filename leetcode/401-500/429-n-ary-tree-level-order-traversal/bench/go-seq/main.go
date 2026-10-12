// Benchmark for #429: mirror of level_order.kara (breadth first, a
// level at a time).
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	val      int64
	children []*Node
}

func levelOrder(root *Node) [][]int64 {
	var levels [][]int64
	var level []*Node
	if root != nil {
		level = append(level, root)
	}
	for len(level) > 0 {
		var row []int64
		var next []*Node
		for _, node := range level {
			row = append(row, node.val)
			next = append(next, node.children...)
		}
		levels = append(levels, row)
		level = next
	}
	return levels
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func buildRandom(i int64, vals []int64, kids [][]int64) *Node {
	node := &Node{val: vals[i]}
	for _, k := range kids[i] {
		node.children = append(node.children, buildRandom(k, vals, kids))
	}
	return node
}

func main() {
	n := int64(10000)
	rounds := int64(200)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(429)
	rows := int64(0)
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		reach := 10 + step(&seed)%1000
		vals := make([]int64, 0, n)
		kids := make([][]int64, 0, n)
		for i := int64(0); i < n; i++ {
			vals = append(vals, step(&seed)%10001)
			kids = append(kids, nil)
			if i > 0 {
				lim := i
				if reach < lim {
					lim = reach
				}
				back := 1 + step(&seed)%lim
				kids[i-back] = append(kids[i-back], i)
			}
		}
		levels := levelOrder(buildRandom(0, vals, kids))
		rows += int64(len(levels))
		for _, row := range levels {
			checksum = (checksum*31 + int64(len(row))*10007 + row[0] + row[len(row)-1]) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d nodes: %d levels, checksum %d\n", rounds, n, rows, checksum)
}
