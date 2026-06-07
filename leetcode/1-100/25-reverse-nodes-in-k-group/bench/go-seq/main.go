// Benchmark workload — Reverse Nodes in k-Group (LeetCode #25), iterative.
// Go single-threaded mirror of bench/iterative.{kara,rs,c}. Idiomatic Go:
// GC-managed pointer-linked nodes — no manual free, no Rc. Same N/K/k and
// full-traversal sink; the per-iteration list is reclaimed by the GC.
// See ../README.md.

package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func reverseKGroup(head *ListNode, k int64) *ListNode {
	dummy := &ListNode{next: head}
	groupPrev := dummy
	for {
		// Probe k nodes ahead; a partial trailing group stays in place.
		probe := groupPrev.next
		var count int64
		for count < k && probe != nil {
			probe = probe.next
			count++
		}
		if count < k {
			break
		}
		groupHead := groupPrev.next
		// Reverse exactly k nodes, prev seeded with the suffix.
		prev := probe
		cur := groupPrev.next
		for j := int64(0); j < k; j++ {
			nxt := cur.next
			cur.next = prev
			prev = cur
			cur = nxt
		}
		groupPrev.next = prev
		groupPrev = groupHead
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
		reversed := reverseKGroup(list, 5)
		total += sumList(reversed)
	}
	fmt.Println(total)
}
