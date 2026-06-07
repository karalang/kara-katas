// Benchmark workload — Swap Nodes in Pairs (LeetCode #24), iterative.
// Go single-threaded mirror of bench/iterative.{kara,rs,c}. Idiomatic Go:
// GC-managed pointer-linked nodes — no manual free, no Rc. Same N/K and
// full-traversal sink; the per-iteration list is reclaimed by the GC.
// See ../README.md.

package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func swapPairs(head *ListNode) *ListNode {
	dummy := &ListNode{next: head}
	prev := dummy
	for prev.next != nil && prev.next.next != nil {
		first := prev.next
		second := first.next
		// Re-link prev → second → first → rest.
		first.next = second.next
		second.next = first
		prev.next = second
		prev = first
	}
	return dummy.next
}

func buildList(count int64) *ListNode {
	if count <= 0 {
		return nil
	}
	head := &ListNode{val: 1}
	tail := head
	for v := int64(2); v <= count; v++ {
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
		list := buildList(nValues)
		swapped := swapPairs(list)
		total += sumList(swapped)
	}
	fmt.Println(total)
}
