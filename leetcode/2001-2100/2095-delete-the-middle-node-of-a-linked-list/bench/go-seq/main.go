// LeetCode #2095: Delete the Middle Node of a Linked List -- Go mirror of
// the ★ arm's benchmark (middle.kara): the same 20000 lists of `*ListNode`,
// each with its middle deleted 50 times by the same two runners.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func deleteMiddle(head *ListNode) *ListNode {
	if head == nil || head.next == nil {
		return nil
	}
	slow := head
	fast := head.next.next
	for fast != nil && fast.next != nil {
		slow = slow.next
		fast = fast.next.next
	}
	slow.next = slow.next.next
	return head
}

func build(m, round int64) *ListNode {
	var head *ListNode
	for j := m - 1; j >= 0; j-- {
		head = &ListNode{(round*7919+j*104729)%100000 + 1, head}
	}
	return head
}

func main() {
	rounds := int64(20000)
	left, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		list := build(1000, r)
		for k := 0; k < 50; k++ {
			list = deleteMiddle(list)
		}
		for cur := list; cur != nil; cur = cur.next {
			left++
			check = (check*31 + cur.val) % 1000000007
		}
	}
	fmt.Printf("%d rounds: %d nodes left, checksum %d\n", rounds, left, check)
}
