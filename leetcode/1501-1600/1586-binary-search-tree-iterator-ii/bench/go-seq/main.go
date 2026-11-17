// LeetCode #1586: Binary Search Tree Iterator II -- the bench in Go,
// mirroring bst_iterator.kara: the lazy in-order stack and the list of
// values met.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

type BSTIterator struct {
	spine []*TreeNode
	seen  []int32
	at    int64
}

func newIterator(root *TreeNode) *BSTIterator {
	it := &BSTIterator{at: -1}
	it.pushLeft(root)
	return it
}

func (it *BSTIterator) pushLeft(node *TreeNode) {
	for node != nil {
		it.spine = append(it.spine, node)
		node = node.Left
	}
}

func (it *BSTIterator) HasNext() bool {
	return it.at+1 < int64(len(it.seen)) || len(it.spine) > 0
}

func (it *BSTIterator) Next() int32 {
	it.at++
	if it.at == int64(len(it.seen)) {
		n := it.spine[len(it.spine)-1]
		it.spine = it.spine[:len(it.spine)-1]
		it.seen = append(it.seen, n.Val)
		it.pushLeft(n.Right)
	}
	return it.seen[it.at]
}

func (it *BSTIterator) HasPrev() bool { return it.at > 0 }

func (it *BSTIterator) Prev() int32 {
	it.at--
	return it.seen[it.at]
}

func insert(root *TreeNode, v int32) bool {
	node := root
	for {
		if v == node.Val {
			return false
		}
		child := &node.Right
		if v < node.Val {
			child = &node.Left
		}
		if *child != nil {
			node = *child
		} else {
			*child = &TreeNode{Val: v}
			return true
		}
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func drawCalls(n, count int64, seed *int64) []int64 {
	at := int64(-1)
	calls := make([]int64, 0, count)
	for i := int64(0); i < count; i++ {
		r := nextRandom(seed) % 6
		if r >= 2 && r <= 4 && at+1 < n {
			at++
			calls = append(calls, 1)
		} else if r == 5 && at > 0 {
			at--
			calls = append(calls, 3)
		} else {
			calls = append(calls, r%2*2)
		}
	}
	return calls
}

func b2i(b bool) int64 {
	if b {
		return 1
	}
	return 0
}

func drive(root *TreeNode, calls []int64) []int64 {
	it := newIterator(root)
	out := make([]int64, 0)
	for _, c := range calls {
		var answer int64
		switch c {
		case 0:
			answer = b2i(it.HasNext())
		case 1:
			answer = int64(it.Next())
		case 2:
			answer = b2i(it.HasPrev())
		default:
			answer = int64(it.Prev())
		}
		out = append(out, answer)
	}
	return out
}

func main() {
	seed := int64(1586)
	var roots []*TreeNode
	var calls [][]int64
	nodes := int64(0)
	for k := 0; k < 20; k++ {
		values := make([]int32, 100000)
		for i := range values {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			values[i] = int32((a*32768 + b) % 1000000)
		}
		root := &TreeNode{Val: values[0]}
		n := int64(1)
		for _, v := range values[1:] {
			if insert(root, v) {
				n++
			}
		}
		nodes += n
		roots = append(roots, root)
		calls = append(calls, drawCalls(n, 300000, &seed))
	}
	check := int64(0)
	for k := range roots {
		for _, answer := range drive(roots[k], calls[k]) {
			check = mix(check, answer)
		}
	}
	fmt.Printf("20 trees of 100000 values: %d nodes, 6000000 calls, checksum %d\n", nodes, check)
}
