// Benchmark workload — Merge Two Sorted Lists (LeetCode #21), iterative.
// Go single-threaded mirror of bench/iterative.{kara,rs,c}. Idiomatic Go:
// GC-managed pointer-linked nodes — no manual free, no Rc. Same N/K, evens/odds
// interleaving, and full-traversal sink; the per-iteration lists are reclaimed
// by the GC. See ../README.md.

package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func mergeTwoLists(l1, l2 *ListNode) *ListNode {
	dummy := &ListNode{}
	tail := dummy
	a, b := l1, l2
	for a != nil && b != nil {
		if a.val <= b.val {
			tail.next = a
			tail = a
			a = a.next
		} else {
			tail.next = b
			tail = b
			b = b.next
		}
	}
	if a != nil {
		tail.next = a
	} else {
		tail.next = b
	}
	return dummy.next
}

func buildList(start, step, count int64) *ListNode {
	if count <= 0 {
		return nil
	}
	head := &ListNode{val: start}
	tail := head
	v := start
	for i := int64(1); i < count; i++ {
		v += step
		node := &ListNode{val: v}
		tail.next = node
		tail = node
	}
	return head
}

func sumList(list *ListNode) int64 {
	var s int64
	for c := list; c != nil; c = c.next {
		s += c.val
	}
	return s
}

func main() {
	const nValues int64 = 100
	const kIters int64 = 500_000

	var total int64
	for k := int64(0); k < kIters; k++ {
		a := buildList(0, 2, nValues)
		b := buildList(1, 2, nValues)
		merged := mergeTwoLists(a, b)
		total += sumList(merged)
	}
	fmt.Println(total)
}
