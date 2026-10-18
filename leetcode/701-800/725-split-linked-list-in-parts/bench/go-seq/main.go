// LeetCode #725: Split Linked List in Parts -- count, then cut in place.
// Benchmark mirror of the Kara star arm: count the nodes, then walk the
// list once, taking each part's head, stepping to its last node and
// cutting the link after it.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func splitListToParts(head *ListNode, k int64) []*ListNode {
	var n int64
	for cur := head; cur != nil; cur = cur.next {
		n++
	}
	size, extra := n/k, n%k
	parts := make([]*ListNode, 0, k)
	cur := head
	for i := int64(0); i < k; i++ {
		parts = append(parts, cur)
		length := size
		if i < extra {
			length = size + 1
		}
		if length > 0 && cur != nil {
			tail := cur
			for s := int64(0); s < length-1; s++ {
				if tail.next != nil {
					tail = tail.next
				}
			}
			cur = tail.next
			tail.next = nil
		}
	}
	return parts
}

// Put the parts back together, starting from part `from` and going round.
func rejoin(parts []*ListNode, from int64) *ListNode {
	k := int64(len(parts))
	var head *ListNode
	for i := k; i > 0; {
		i--
		first := parts[(from+i)%k]
		if first != nil {
			tail := first
			for tail.next != nil {
				tail = tail.next
			}
			tail.next = head
			head = first
		}
	}
	return head
}

func main() {
	seed := int64(725)
	lists := make([]*ListNode, 0, 20)
	for d := 0; d < 20; d++ {
		var head *ListNode
		for j := 0; j < 1000; j++ {
			head = &ListNode{val: nextRandom(&seed) % 1000, next: head}
		}
		lists = append(lists, head)
	}
	var hash int64
	for round := int64(0); round < 5000; round++ {
		for d := int64(0); d < 20; d++ {
			k := 1 + (round*7+d)%50
			parts := splitListToParts(lists[d], k)
			for _, p := range parts {
				var v int64
				if p != nil {
					v = p.val + 1
				}
				hash = (hash*31 + v) % 1000000007
			}
			lists[d] = rejoin(parts, round%k)
		}
	}
	fmt.Printf("5000 rounds of 20 lists of 1000 numbers: hash %d\n", hash)
}
