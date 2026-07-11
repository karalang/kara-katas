// Benchmark workload — Reverse Linked List II (LeetCode #92).
// Go mirror of ../reverse_between.kara. Plain *ListNode singly-linked list (GC). Each
// iteration builds a fresh M=200 list, reverses a ~100-node window (shifting start),
// folds the result. Same M/K.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func reverseBetween(head *ListNode, left, right int64) *ListNode {
	dummy := &ListNode{next: head}
	prev := dummy
	for i := int64(1); i < left; i++ {
		if prev.next != nil {
			prev = prev.next
		}
	}
	cur := prev.next
	if cur != nil {
		for j := left; j < right; j++ {
			nxt := cur.next
			if nxt != nil {
				cur.next = nxt.next
				nxt.next = prev.next
				prev.next = nxt
			}
		}
	}
	return dummy.next
}

func build(m, seed int64) *ListNode {
	dummy := &ListNode{val: -1}
	tail := dummy
	for j := int64(0); j < m; j++ {
		node := &ListNode{val: (j + seed) % 1000}
		tail.next = node
		tail = node
	}
	return dummy.next
}

func fold(list *ListNode, seed int64) int64 {
	a := seed
	c := list
	for c != nil {
		a = (a*131 + (c.val + 1000)) % 1000000007
		c = c.next
	}
	return a
}

func main() {
	const m = 200
	const total = 178000
	const modulus = 1000000007
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		list := build(m, k)
		left := 1 + (k % 50)
		right := left + 100
		r := reverseBetween(list, left, right)
		sum = (sum*131 + fold(r, k)) % modulus
	}
	fmt.Println(sum)
}
