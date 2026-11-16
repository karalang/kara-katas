// LeetCode #1171: Remove Zero Sum Consecutive Nodes from Linked List -- the
// ★ arm's bench in Go: prefix sums in two passes, the last node of each
// running sum kept in a map. The same 32 lists and 400 rounds.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func removeZeroSumSublists(head *ListNode) *ListNode {
	dummy := &ListNode{0, head}
	last := map[int64]*ListNode{}
	var sum int64
	for cur := dummy; cur != nil; cur = cur.Next {
		sum += cur.Val
		last[sum] = cur
	}
	sum = 0
	for cur := dummy; cur != nil; cur = cur.Next {
		sum += cur.Val
		cur.Next = last[sum].Next
	}
	return dummy.Next
}

var seed int64 = 1171

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue(kind int) int64 {
	switch kind {
	case 0:
		return nextRandom()%5 - 2
	case 1:
		return nextRandom()%11 - 5
	case 2:
		return nextRandom()%101 - 50
	default:
		size := 1 + nextRandom()%3
		if nextRandom()%2 == 0 {
			return size
		}
		return -size
	}
}

func main() {
	rounds := 400
	lists := make([][]int64, 32)
	for l := 0; l < 32; l++ {
		lists[l] = make([]int64, 1000)
		for i := range lists[l] {
			lists[l][i] = randomValue(l % 4)
		}
	}
	var kept, check int64
	for r := 0; r < rounds; r++ {
		for l := 0; l < 32; l++ {
			i := nextRandom() % 1000
			lists[l][i] = randomValue(l % 4)
			var head *ListNode
			for k := 999; k >= 0; k-- {
				head = &ListNode{lists[l][k], head}
			}
			for cur := removeZeroSumSublists(head); cur != nil; cur = cur.Next {
				kept++
				check = (check*131 + cur.Val + 1001) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 32 lists of 1000 values: %d kept, checksum %d\n", rounds, kept, check)
}
