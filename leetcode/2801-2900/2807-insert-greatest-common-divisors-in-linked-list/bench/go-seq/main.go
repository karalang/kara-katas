// LeetCode #2807: Insert Greatest Common Divisors in Linked List -- the
// bench in Go: the ★ arm over 200 lists of 5000 values up to 1000, all
// drawn first, then each built afresh and answered 10 times.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func insertGreatestCommonDivisors(head *ListNode) *ListNode {
	for cur := head; cur != nil && cur.Next != nil; {
		after := cur.Next
		cur.Next = &ListNode{Val: gcd(cur.Val, after.Val), Next: after}
		cur = after
	}
	return head
}

var seed int64 = 2807

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 200
	rounds := 10
	cases := make([][]int64, count)
	for t := 0; t < count; t++ {
		step := int64(1)
		if t%2 == 0 {
			step = 12
		}
		cases[t] = make([]int64, 5000)
		for i := range cases[t] {
			cases[t][i] = (nextRandom()%(1000/step) + 1) * step
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, values := range cases {
			var head *ListNode
			for i := len(values) - 1; i >= 0; i-- {
				head = &ListNode{Val: values[i], Next: head}
			}
			var sum int64
			for cur := insertGreatestCommonDivisors(head); cur != nil; cur = cur.Next {
				sum += cur.Val
			}
			total += sum
			check = (check*31 + sum + r) % 1000000007
		}
	}
	fmt.Printf("%d lists of 5000, %d rounds: values sum to %d, checksum %d\n", count, rounds, total, check)
}
