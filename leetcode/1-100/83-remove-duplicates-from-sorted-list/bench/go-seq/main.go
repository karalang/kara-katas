// Benchmark workload — Remove Duplicates from Sorted List (LeetCode #83).
// Go mirror of ../remove_duplicates_list.kara. Plain *ListNode singly-linked list
// (GC-managed). Each iteration builds a fresh list (M=300, every value duplicated),
// runs the keep-one dedup, and folds the survivors through a rolling polynomial hash.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func deleteDuplicates(head *ListNode) *ListNode {
	cur := head
	for cur != nil {
		if cur.next != nil {
			if cur.val == cur.next.val {
				cur.next = cur.next.next
			} else {
				cur = cur.next
			}
		} else {
			break
		}
	}
	return head
}

func build(m, dup int64) *ListNode {
	dummy := &ListNode{val: -1}
	tail := dummy
	for v := int64(0); v < m; v++ {
		for d := int64(0); d < dup; d++ {
			node := &ListNode{val: v}
			tail.next = node
			tail = node
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
	const dup = 2
	const total = 70000
	const modulus = 1000000007
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		list := build(m, dup)
		dd := deleteDuplicates(list)
		sum = (sum*131 + fold(dd, k)) % modulus
	}
	fmt.Println(sum)
}
