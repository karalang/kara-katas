// LeetCode 297 benchmark lane — Go mirror of treecodec.kara.
//
// Same algorithm, same tree shape, same sink: build one balanced 200k-node
// tree, then 24 chained serialize/deserialize round trips, hashing every
// encoded string. See the .kara file's header for the workload rationale.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type Node struct {
	val         int64
	left, right *Node
}

func build(vals []int64, lo, hi int) *Node {
	if lo >= hi {
		return nil
	}
	mid := lo + (hi-lo)/2
	l := build(vals, lo, mid)
	r := build(vals, mid+1, hi)
	return &Node{val: vals[mid], left: l, right: r}
}

func serInto(t *Node, out *strings.Builder) {
	if out.Len() > 0 {
		out.WriteByte(',')
	}
	if t == nil {
		out.WriteByte('#')
		return
	}
	out.WriteString(strconv.FormatInt(t.val, 10))
	serInto(t.left, out)
	serInto(t.right, out)
}

func serialize(t *Node) string {
	var b strings.Builder
	serInto(t, &b)
	return b.String()
}

func deAt(toks []string, i *int) *Node {
	tok := toks[*i]
	*i++
	if tok == "#" {
		return nil
	}
	v, err := strconv.ParseInt(tok, 10, 64)
	if err != nil {
		v = 0
	}
	l := deAt(toks, i)
	r := deAt(toks, i)
	return &Node{val: v, left: l, right: r}
}

func deserialize(s string) *Node {
	toks := strings.Split(s, ",")
	i := 0
	return deAt(toks, &i)
}

func hashString(s string, seed int64) int64 {
	h := seed
	for k := 0; k < len(s); k++ {
		h = (h*131 + int64(s[k])) % 1000000007
	}
	return h
}

func main() {
	const n = 200000
	const rounds = 24

	vals := make([]int64, 0, n)
	var state int64 = 12345
	for i := 0; i < n; i++ {
		state = (state*1103515245 + 12345) & 0x7fffffff
		vals = append(vals, state%1000003-500000)
	}

	tree := build(vals, 0, n)
	var checksum int64

	for r := 0; r < rounds; r++ {
		s := serialize(tree)
		checksum = hashString(s, checksum)
		tree = deserialize(s)
	}

	fmt.Printf("nodes %d rounds %d checksum %d\n", n, rounds, checksum)
}
