// LeetCode 298 benchmark lane — Go mirror of consecpath.kara.
//
// Same tree, same passes, same sink: build one perfect depth-20 tree, then 40
// full traversals with steps 1..40. See the .kara file's header for the
// workload rationale.
package main

import "fmt"

type Node struct {
	val         int64
	left, right *Node
}

func build(depth int, parentVal int64, state *int64) *Node {
	if depth <= 0 {
		return nil
	}
	*state = (*state*1103515245 + 12345) & 0x7fffffff
	v := parentVal + *state%3 - 1
	l := build(depth-1, v, state)
	r := build(depth-1, v, state)
	return &Node{val: v, left: l, right: r}
}

func down(t *Node, step int64, best *int64) int64 {
	if t == nil {
		return 0
	}
	l := down(t.left, step, best)
	r := down(t.right, step, best)
	var run int64 = 1
	if t.left != nil && t.left.val == t.val+step && l+1 > run {
		run = l + 1
	}
	if t.right != nil && t.right.val == t.val+step && r+1 > run {
		run = r + 1
	}
	if run > *best {
		*best = run
	}
	return run
}

func longestWithStep(t *Node, step int64) int64 {
	var best int64
	down(t, step, &best)
	return best
}

func main() {
	const depth = 20
	const passes = 40

	var state int64 = 12345
	tree := build(depth, 0, &state)

	var checksum int64
	for d := 1; d <= passes; d++ {
		checksum = (checksum*31 + longestWithStep(tree, int64(d))) % 1000000007
	}

	fmt.Printf("depth %d passes %d checksum %d\n", depth, passes, checksum)
}
