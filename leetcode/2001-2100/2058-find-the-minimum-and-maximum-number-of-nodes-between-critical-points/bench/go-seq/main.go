// LeetCode #2058: Find the Minimum and Maximum Number of Nodes Between
// Critical Points -- Go mirror of the ★ arm's benchmark (critical.kara):
// the same 50 lists of 100000 values, each built node by node and
// answered by one walk; the collector frees them.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

var seed int64 = 2058

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func nodesBetweenCriticalPoints(head *ListNode) [2]int64 {
	if head == nil {
		return [2]int64{-1, -1}
	}
	before := head.val
	var at, first, last, nearest int64 = 1, -1, -1, -1
	for node := head.next; node != nil; node, at = node.next, at+1 {
		if after := node.next; after != nil {
			v := node.val
			if (v > before && v > after.val) || (v < before && v < after.val) {
				if first < 0 {
					first = at
				} else if nearest < 0 || at-last < nearest {
					nearest = at - last
				}
				last = at
			}
		}
		before = node.val
	}
	if nearest < 0 {
		return [2]int64{-1, -1}
	}
	return [2]int64{nearest, last - first}
}

func main() {
	tops := []int64{2, 3, 10, 100000}
	var total, check int64
	for t := 0; t < 50; t++ {
		top := tops[t%4]
		var head *ListNode
		for i := 0; i < 100000; i++ {
			head = &ListNode{val: nextRandom()%top + 1, next: head}
		}
		d := nodesBetweenCriticalPoints(head)
		total += d[0] + d[1]
		check = (check*31 + d[0] + 2) % 1000000007
		check = (check*31 + d[1] + 2) % 1000000007
	}
	fmt.Printf("50 lists: sum %d, checksum %d\n", total, check)
}
