// Benchmark workload — Remove Nth Node From End (LeetCode #19).
// Go single-threaded mirror of bench/remove_nth.{kara,rs,c}. Idiomatic Go:
// GC-managed pointer-linked nodes — no manual free, no Rc. Same N/K, append
// list-builder, rotating removal position, and sink; the removed node and
// the per-iteration chain are reclaimed by the GC. See ../README.md.

package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func removeNthFromEnd(head *ListNode, n int64) *ListNode {
	dummy := &ListNode{next: head}

	fast := head
	for i := int64(0); i < n; i++ {
		if fast != nil {
			fast = fast.next
		}
	}

	slow := dummy
	for fast != nil {
		fast = fast.next
		if slow.next != nil {
			slow = slow.next
		}
	}

	if slow.next != nil {
		slow.next = slow.next.next
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

func main() {
	const nValues int64 = 100
	const kIters int64 = 500_000

	var sum int64
	for k := int64(0); k < kIters; k++ {
		list := buildList(nValues)
		n := (k % nValues) + 1
		out := removeNthFromEnd(list, n)
		if out != nil {
			sum += out.val
		}
	}
	fmt.Println(sum)
}
