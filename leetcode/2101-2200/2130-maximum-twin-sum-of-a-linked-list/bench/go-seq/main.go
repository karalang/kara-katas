// LeetCode #2130: Maximum Twin Sum of a Linked List -- the benchmark, the
// same algorithm as twins.kara.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func pairSum(head *ListNode) int64 {
	values := []int64{}
	for n := head; n != nil; n = n.next {
		values = append(values, n.val)
	}
	l := len(values)
	var best int64
	for i := 0; i < l/2; i++ {
		if s := values[i] + values[l-1-i]; s > best {
			best = s
		}
	}
	return best
}

var seed int64 = 2130

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	lists := make([]*ListNode, 10)
	for k := range lists {
		var head *ListNode
		for i := 0; i < n; i++ {
			hi := nextRandom()
			head = &ListNode{val: (hi*32768+nextRandom())%100000 + 1, next: head}
		}
		lists[k] = head
	}
	var total, check int64
	for round := int64(0); round < 50; round++ {
		for k := 0; k < 10; k++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % n
			node := lists[k]
			for i := int64(0); i < at; i++ {
				node = node.next
			}
			node.val = nextRandom()%200000 + 1
			sum := pairSum(lists[k])
			total += sum
			check = (check*31 + sum + round) % 1000000007
		}
	}
	fmt.Printf("500 solves: %d in all, checksum %d\n", total, check)
}
