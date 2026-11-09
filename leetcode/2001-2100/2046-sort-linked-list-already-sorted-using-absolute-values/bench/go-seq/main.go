// LeetCode #2046 -- the ★ arm as a benchmark; mirror of ../sort.kara, the
// nodes *ListNode.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func sortLinkedList(head *ListNode) *ListNode {
	if head == nil {
		return nil
	}
	front, prev, cur := head, head, head.next
	for cur != nil {
		node := cur
		cur = node.next
		if node.val < 0 {
			prev.next = node.next
			node.next = front
			front = node
		} else {
			prev = node
		}
	}
	return front
}

func build(m, round int64) *ListNode {
	var head *ListNode
	for j := m - 1; j >= 0; j-- {
		v := j / 2
		if (7*j+round)%3 == 0 {
			v = -(j / 2)
		}
		head = &ListNode{val: v, next: head}
	}
	return head
}

func main() {
	var rounds, m, negatives, check int64 = 20000, 1000, 0, 0
	for r := int64(0); r < rounds; r++ {
		for cur := sortLinkedList(build(m, r)); cur != nil; cur = cur.next {
			if cur.val < 0 {
				negatives++
			}
			check = (check*31 + cur.val + 1000) % 1000000007
		}
	}
	fmt.Printf("%d rounds: %d negatives, checksum %d\n", rounds, negatives, check)
}
