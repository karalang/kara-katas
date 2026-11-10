// LeetCode #2074: Reverse Nodes in Even Length Groups -- Go mirror of the
// ★ arm's benchmark (groups.kara): 2000 rounds, each a fresh list of 10000
// values turned group by group in place and folded into a checksum.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func reverseEvenLengthGroups(head *ListNode) *ListNode {
	if head == nil {
		return nil
	}
	before := head
	var want int64 = 2
	for before.next != nil {
		start := before.next
		end, cur := start, start
		var length int64
		for length < want && cur != nil {
			length++
			end = cur
			cur = cur.next
		}
		if length%2 == 0 {
			turned, rest := end.next, start
			for i := int64(0); i < length; i++ {
				node := rest
				rest = node.next
				node.next = turned
				turned = node
			}
			before.next = turned
			before = start
		} else {
			before = end
		}
		want++
	}
	return head
}

func build(m, round int64) *ListNode {
	var head *ListNode
	for j := m - 1; j >= 0; j-- {
		head = &ListNode{(j*7919 + round) % 100001, head}
	}
	return head
}

func main() {
	var check int64
	for r := int64(0); r < 2000; r++ {
		for cur := reverseEvenLengthGroups(build(10000+r%7, r)); cur != nil; cur = cur.next {
			check = (check*31 + cur.val) % 1000000007
		}
	}
	fmt.Printf("2000 rounds: checksum %d\n", check)
}
