// LeetCode #1721: Swapping Nodes in a Linked List -- the bench
// (swap.kara): the kth node found, then a runner from it to the last node
// drags a second cursor from the head to the kth node from the end.
package main

import "fmt"

type listNode struct {
	val  int64
	next *listNode
}

func swapNodes(head *listNode, k int64) *listNode {
	first := head
	for i := int64(1); i < k; i++ {
		first = first.next
	}
	second := head
	runner := first
	for runner.next != nil {
		runner = runner.next
		second = second.next
	}
	first.val, second.val = second.val, first.val
	return head
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func build(values []int64) *listNode {
	var head *listNode
	for i := len(values) - 1; i >= 0; i-- {
		head = &listNode{val: values[i], next: head}
	}
	return head
}

func main() {
	count := 10
	var rounds int64 = 100
	var n int64 = 100000
	var seed int64 = 1721
	lists := make([]*listNode, count)
	for c := 0; c < count; c++ {
		values := make([]int64, n)
		for i := range values {
			values[i] = nextRandom(&seed) % 101
		}
		lists[c] = build(values)
	}
	ks := make([]int64, int64(count)*rounds)
	for i := range ks {
		ks[i] = wide(&seed)%n + 1
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			head := swapNodes(lists[c], ks[r*int64(count)+int64(c)])
			sum += head.val
			check = (check*31 + head.val + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of %d nodes, %d rounds: heads sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
