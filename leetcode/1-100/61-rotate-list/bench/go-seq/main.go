// Benchmark workload — Rotate List (LeetCode #61).
// Go single-threaded mirror of bench/rotate_list.{kara,rs,c}. Idiomatic Go:
// GC-managed pointer-linked nodes — no manual free, no Rc. Same N/K, append
// list-builder, rotation sweep r = k % (2*N), and sink; the per-iteration
// chain is reclaimed by the GC. See ../README.md § Benchmarks.

package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func rotateRight(head *ListNode, k int64) *ListNode {
	var length int64 = 0
	cur := head
	var tail *ListNode = nil
	for cur != nil {
		length++
		tail = cur
		cur = cur.next
	}

	if length == 0 {
		return nil
	}
	shift := k % length
	if shift == 0 {
		return head
	}

	tail.next = head // close the ring

	steps := length - shift - 1
	newTail := head
	for i := int64(0); i < steps; i++ {
		if newTail != nil {
			newTail = newTail.next
		}
	}

	result := head
	if newTail != nil {
		result = newTail.next
		newTail.next = nil // sever the ring
	}
	return result
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
	const span int64 = 200 // 2*N
	const kIters int64 = 500_000

	var sum int64
	for k := int64(0); k < kIters; k++ {
		list := buildList(nValues)
		r := k % span
		out := rotateRight(list, r)
		if out != nil {
			sum += out.val
		}
	}
	fmt.Println(sum)
}
