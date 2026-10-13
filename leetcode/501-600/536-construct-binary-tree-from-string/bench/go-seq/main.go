// Benchmark for #536: the ★ arm (recursive descent); see
// ../../README.md § Benchmarks. Mirrors str2tree.kara.
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

// The tree that starts at byte *i, leaving *i just past it.
func parse(b string, i *int) *TreeNode {
	sign := int64(1)
	if b[*i] == '-' {
		sign = -1
		*i++
	}
	val := int64(0)
	for *i < len(b) && b[*i] >= '0' && b[*i] <= '9' {
		val = val*10 + int64(b[*i]-'0')
		*i++
	}
	n := &TreeNode{Val: sign * val}
	if *i < len(b) && b[*i] == '(' {
		*i++
		n.Left = parse(b, i)
		*i++
	}
	if *i < len(b) && b[*i] == '(' {
		*i++
		n.Right = parse(b, i)
		*i++
	}
	return n
}

func str2tree(s string) *TreeNode {
	if len(s) == 0 {
		return nil
	}
	i := 0
	return parse(s, &i)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomTree(seed *int64, n int64) *TreeNode {
	if n == 0 {
		return nil
	}
	val := nextRandom(seed)%2001 - 1000
	rest := n - 1
	var left int64
	if rest == 0 {
		left = 0
	} else if nextRandom(seed)%3 == 0 {
		left = rest
	} else {
		left = 1 + nextRandom(seed)%rest
	}
	l := randomTree(seed, left)
	r := randomTree(seed, rest-left)
	return &TreeNode{Val: val, Left: l, Right: r}
}

func render(n *TreeNode, out *strings.Builder) {
	if n == nil {
		return
	}
	out.WriteString(strconv.FormatInt(n.Val, 10))
	if n.Left != nil {
		out.WriteByte('(')
		render(n.Left, out)
		out.WriteByte(')')
	}
	if n.Right != nil {
		out.WriteByte('(')
		render(n.Right, out)
		out.WriteByte(')')
	}
}

func walk(n *TreeNode, stats *[2]int64) {
	if n == nil {
		return
	}
	stats[0]++
	stats[1] = (stats[1]*31 + n.Val + 1000) % 1000000007
	walk(n.Left, stats)
	walk(n.Right, stats)
}

func main() {
	seed := int64(536)
	strs := []string{}
	for k := 0; k < 20; k++ {
		tree := randomTree(&seed, 5500)
		var b strings.Builder
		render(tree, &b)
		strs = append(strs, b.String())
	}
	rounds := 100
	var stats [2]int64
	for r := 0; r < rounds; r++ {
		for _, s := range strs {
			walk(str2tree(s), &stats)
		}
	}
	fmt.Printf("%d strings, %d rounds: %d nodes, checksum %d\n", len(strs), rounds, stats[0], stats[1])
}
