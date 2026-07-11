// Benchmark workload — Partition List (LeetCode #86), SEQ lane.
// Go mirror of ../partition_list.kara. Plain *ListNode singly-linked list (GC-managed).
// Each iteration builds a fresh M=200 list, stably partitions around x=50, and adds
// the fold into an associative sum. Same M/K. The go-par/ sibling parallelises with
// goroutines.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func partition(head *ListNode, x int64) *ListNode {
	var lessDummy, greaterDummy ListNode
	lessTail := &lessDummy
	greaterTail := &greaterDummy
	cur := head
	for cur != nil {
		nxt := cur.next
		cur.next = nil
		if cur.val < x {
			lessTail.next = cur
			lessTail = cur
		} else {
			greaterTail.next = cur
			greaterTail = cur
		}
		cur = nxt
	}
	lessTail.next = greaterDummy.next
	return lessDummy.next
}

func build(m, seed int64) *ListNode {
	var dummy ListNode
	tail := &dummy
	for j := int64(0); j < m; j++ {
		node := &ListNode{val: (j*7 + seed) % 100}
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
	const total = 170000
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		list := build(m, k)
		p := partition(list, 50)
		sum += fold(p, k)
	}
	fmt.Println(sum)
}
