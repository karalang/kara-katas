// LeetCode #95: Unique Binary Search Trees II — recursive divide & conquer.
// Go mirror of generate_trees.kara. Same algorithm: for each root value i in
// [lo, hi], cross-product every left subtree (lo..i-1) with every right subtree
// (i+1..hi). Kara shares subtree instances via RC; this uses GC-managed *Node
// and deep-copies each (left, right) pair into the new root — the same set of
// trees, the same canonical preorder serialization and fold, so stdout is
// byte-identical.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

const mod = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func copyTree(n *Node) *Node {
	if n == nil {
		return nil
	}
	return &Node{val: n.val, left: copyTree(n.left), right: copyTree(n.right)}
}

// buildAll returns every BST over the contiguous value range [lo, hi].
func buildAll(lo, hi int64) []*Node {
	result := []*Node{}
	if lo > hi {
		return append(result, nil)
	}
	for i := lo; i <= hi; i++ {
		lefts := buildAll(lo, i-1)
		rights := buildAll(i+1, hi)
		for _, l := range lefts {
			for _, r := range rights {
				result = append(result, &Node{val: i, left: copyTree(l), right: copyTree(r)})
			}
		}
	}
	return result
}

// serialize writes the canonical preorder form with '#' null markers.
func serialize(n *Node, out *strings.Builder) {
	if n == nil {
		out.WriteString("#,")
		return
	}
	out.WriteString(strconv.FormatInt(n.val, 10))
	out.WriteByte(',')
	serialize(n.left, out)
	serialize(n.right, out)
}

// Benchmark workload: 250 repeats of building every BST over 1..8, folding each
// tree's canonical preorder serialization into a rolling hash. See ../README.md.
func benchReport(n int64, acc *int64) {
	trees := buildAll(1, n)
	count := int64(len(trees))
	a := (*acc*131 + (count + 1)) % mod
	for _, tree := range trees {
		var sb strings.Builder
		serialize(tree, &sb)
		for _, b := range []byte(sb.String()) {
			a = (a*131 + int64(b)) % mod
		}
		a = (a*131 + 7) % mod
	}
	*acc = a
}

func main() {
	var acc int64 = 0
	for rep := 0; rep < 250; rep++ {
		for n := int64(1); n <= 8; n++ {
			benchReport(n, &acc)
		}
	}
	fmt.Printf("%d\n", acc)
}
