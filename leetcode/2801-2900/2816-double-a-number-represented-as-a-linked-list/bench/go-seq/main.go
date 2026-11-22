// LeetCode #2816: Double a Number Represented as a Linked List -- the
// bench in Go: the ★ arm over 200 numbers of 10^4 digits, all drawn
// first, then each built as a list and doubled 20 times, the list read
// back after each.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func doubleIt(head *ListNode) *ListNode {
	if head == nil {
		return nil
	}
	if head.Val > 4 {
		head = &ListNode{0, head}
	}
	for node := head; node != nil; node = node.Next {
		node.Val = node.Val * 2 % 10
		if node.Next != nil && node.Next.Val > 4 {
			node.Val++
		}
	}
	return head
}

func build(values []int64) *ListNode {
	var head *ListNode
	for i := len(values) - 1; i >= 0; i-- {
		head = &ListNode{values[i], head}
	}
	return head
}

var seed int64 = 2816

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds, n := 200, 20, 10000
	numbers := make([][]int64, count)
	for c := range numbers {
		digits := make([]int64, n)
		for i := range digits {
			digits[i] = nextRandom() % 10
		}
		if digits[0] == 0 {
			digits[0] = nextRandom()%9 + 1
		}
		numbers[c] = digits
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, digits := range numbers {
			h := r
			for node := doubleIt(build(digits)); node != nil; node = node.Next {
				total += node.Val
				h = (h*131 + node.Val) % 1000000007
			}
			check = (check*31 + h) % 1000000007
		}
	}
	fmt.Printf("%d numbers of %d digits, %d rounds: digits sum to %d, checksum %d\n", count, n, rounds, total, check)
}
