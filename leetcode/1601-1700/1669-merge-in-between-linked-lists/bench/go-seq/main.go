// LeetCode #1669: Merge In Between Linked Lists -- the bench's Go mirror: the
// ★ arm on one list of 100000 nodes, 10000 times cut at a random place, 1
// to 8 nodes taken out and a new list of 1 to 8 put in, every cut and value
// drawn first.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func mergeInBetween(list1 *ListNode, a, b int64, list2 *ListNode) *ListNode {
	before := list1
	for i := int64(1); i < a; i++ {
		before = before.Next
	}
	after := before.Next
	for i := a; i <= b; i++ {
		after = after.Next
	}
	last := list2
	for last.Next != nil {
		last = last.Next
	}
	before.Next = list2
	last.Next = after
	return list1
}

var seed int64 = 1669

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func build(values []int64) *ListNode {
	var head *ListNode
	for i := len(values) - 1; i >= 0; i-- {
		head = &ListNode{Val: values[i], Next: head}
	}
	return head
}

func main() {
	const start = 100000
	const rounds = 10000
	values := make([]int64, start)
	for i := range values {
		values[i] = (nextRandom() * 32768 + nextRandom()) % 1000001
	}
	length := int64(start)
	type cut struct {
		a, b  int64
		list2 []int64
	}
	cuts := make([]cut, 0, rounds)
	for r := 0; r < rounds; r++ {
		m := nextRandom()%8 + 1
		a := (nextRandom()*32768+nextRandom())%(length-2) + 1
		b := a + nextRandom()%min(8, length-1-a)
		list2 := make([]int64, m)
		for i := range list2 {
			list2[i] = (nextRandom() * 32768 + nextRandom()) % 1000001
		}
		length += m - (b - a + 1)
		cuts = append(cuts, cut{a, b, list2})
	}
	list := build(values)
	for _, c := range cuts {
		list = mergeInBetween(list, c.a, c.b, build(c.list2))
	}
	var nodes, check int64
	for cur := list; cur != nil; cur = cur.Next {
		nodes++
		check = (check*31 + cur.Val + 1) % 1000000007
	}
	fmt.Printf("%d nodes, %d merges: %d nodes, checksum %d\n", start, rounds, nodes, check)
}
