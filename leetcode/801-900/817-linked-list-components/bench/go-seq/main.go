// Benchmark for #817: Linked List Components -- mirror of the ★ arm (count
// the ends), with the same workload as linked_list_components.kara.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func numComponents(head *ListNode, nums []int64) int64 {
	wanted := make(map[int64]bool, len(nums))
	for _, v := range nums {
		wanted[v] = true
	}
	count := int64(0)
	for node := head; node != nil; node = node.Next {
		if wanted[node.Val] && (node.Next == nil || !wanted[node.Next.Val]) {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const n int64 = 10000
	const rounds int64 = 8000
	seed := int64(817)
	lists := make([]*ListNode, count)
	inside := make([][]int64, count)
	outside := make([][]int64, count)
	for g := 0; g < count; g++ {
		order := make([]int64, n)
		for v := int64(0); v < n; v++ {
			order[v] = v
		}
		for i := int64(0); i < n; i++ {
			j := i + nextRandom(&seed)%(n-i)
			order[i], order[j] = order[j], order[i]
		}
		var head *ListNode
		for k := int64(0); k < n; k++ {
			head = &ListNode{Val: order[n-1-k], Next: head}
		}
		lists[g] = head
		for i := int64(0); i < n; i++ {
			j := i + nextRandom(&seed)%(n-i)
			order[i], order[j] = order[j], order[i]
		}
		m := 1 + nextRandom(&seed)%(n-1)
		inside[g] = append([]int64{}, order[:m]...)
		outside[g] = append([]int64{}, order[m:]...)
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % count
		a := nextRandom(&seed) % int64(len(inside[g]))
		b := nextRandom(&seed) % int64(len(outside[g]))
		inside[g][a], outside[g][b] = outside[g][b], inside[g][a]
		answer := numComponents(lists[g], inside[g])
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds of %d nodes: total %d, checksum %d\n", rounds, n, total, checksum)
}
