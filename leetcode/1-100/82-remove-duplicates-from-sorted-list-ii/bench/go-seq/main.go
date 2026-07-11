// Benchmark workload — Remove Duplicates from Sorted List II (LeetCode #82).
// Go mirror of ../remove_duplicates_ii_list.kara. Plain *ListNode singly-linked list
// (GC-managed). Each iteration builds a fresh list (even values duplicated, odd
// single), runs deleteDuplicates, and folds the survivors through a rolling
// polynomial hash. Same M/K pattern.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func deleteDuplicates(head *ListNode) *ListNode {
	dummy := &ListNode{val: 0, next: head}
	prev := dummy
	cur := dummy.next
	for cur != nil {
		isDup := cur.next != nil && cur.val == cur.next.val
		if isDup {
			v := cur.val
			runner := cur
			for runner != nil && runner.val == v {
				runner = runner.next
			}
			prev.next = runner
			cur = runner
		} else {
			prev = cur
			cur = cur.next
		}
	}
	return dummy.next
}

func build(m int64) *ListNode {
	dummy := &ListNode{val: -1}
	tail := dummy
	for v := int64(0); v < m; v++ {
		node := &ListNode{val: v}
		tail.next = node
		tail = node
		if v%2 == 0 {
			d := &ListNode{val: v}
			tail.next = d
			tail = d
		}
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
	const m = 300
	const total = 61000
	const modulus = 1000000007
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		list := build(m)
		dedup := deleteDuplicates(list)
		sum = (sum*131 + fold(dedup, k)) % modulus
	}
	fmt.Println(sum)
}
