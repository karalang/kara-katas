// Benchmark workload — Merge k Sorted Lists (LeetCode #23), divide and
// conquer. Go single-threaded mirror of bench/divide_and_conquer.{kara,rs,c}.
// Idiomatic Go: GC-managed pointer-linked nodes — no manual free, no Rc.
// Same k/N/K, stride-k interleaving, and full-traversal sink; the
// per-iteration lists are reclaimed by the GC. See ../README.md.

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

func mergeKLists(lists []*ListNode) *ListNode {
	k := len(lists)
	if k == 0 {
		return nil
	}
	for interval := 1; interval < k; interval *= 2 {
		for i := 0; i+interval < k; i += 2 * interval {
			lists[i] = mergeTwoLists(lists[i], lists[i+interval])
		}
	}
	return lists[0]
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
	const kLists int64 = 8
	const nValues int64 = 128
	const kIters int64 = 100_000

	var total int64
	for k := int64(0); k < kIters; k++ {
		lists := make([]*ListNode, 0, kLists)
		for j := int64(0); j < kLists; j++ {
			lists = append(lists, buildList(j, kLists, nValues))
		}
		total += sumList(mergeKLists(lists))
	}
	fmt.Println(total)
}
