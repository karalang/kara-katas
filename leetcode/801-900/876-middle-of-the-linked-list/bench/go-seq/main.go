// LeetCode #876 bench: Go mirror of middle_node.kara (the ★ arm, slow
// and fast pointers) on the same 2,000,000 searches.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func middleNode(head *ListNode) *ListNode {
	slow, fast := head, head
	for fast != nil {
		after := fast.Next
		if after == nil {
			break
		}
		fast = after.Next
		if slow != nil {
			slow = slow.Next
		}
	}
	return slow
}

var seed int64 = 876

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func fromValues(values []int64) *ListNode {
	var head *ListNode
	for k := len(values) - 1; k >= 0; k-- {
		head = &ListNode{Val: values[k], Next: head}
	}
	return head
}

func main() {
	lists := make([]*ListNode, 0, 2000)
	for i := 0; i < 2000; i++ {
		n := nextRandom()%100 + 1
		values := make([]int64, n)
		for j := range values {
			values[j] = nextRandom()%100 + 1
		}
		lists = append(lists, fromValues(values))
	}
	var total, check int64
	for k := 0; k < 2000000; k++ {
		if m := middleNode(lists[(k*7+k/2000)%2000]); m != nil {
			total += m.Val
			check = (check*131 + m.Val) % 1000000007
		}
	}
	fmt.Printf("2000000 searches over 2000 lists: middle values sum to %d, checksum %d\n", total, check)
}
