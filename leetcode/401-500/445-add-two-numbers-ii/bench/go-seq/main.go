// Benchmark for #445: mirror of add_two_numbers.kara (two stacks) on 100
// random numbers of 1,000 to 2,000 digits, built once; 60 rounds add each
// to the next.
package main

import "fmt"

type ListNode struct {
	Val  int64
	Next *ListNode
}

func addTwoNumbers(l1, l2 *ListNode) *ListNode {
	a := []int64{}
	for n := l1; n != nil; n = n.Next {
		a = append(a, n.Val)
	}
	b := []int64{}
	for n := l2; n != nil; n = n.Next {
		b = append(b, n.Val)
	}
	var sum *ListNode
	carry := int64(0)
	for len(a) > 0 || len(b) > 0 || carry > 0 {
		digit := carry
		if len(a) > 0 {
			digit += a[len(a)-1]
			a = a[:len(a)-1]
		}
		if len(b) > 0 {
			digit += b[len(b)-1]
			b = b[:len(b)-1]
		}
		sum = &ListNode{Val: digit % 10, Next: sum}
		carry = digit / 10
	}
	return sum
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds int64 = 100, 60
	seed := int64(445)
	numbers := make([]*ListNode, 0, count)
	for c := int64(0); c < count; c++ {
		length := 1000 + nextRandom(&seed)%1001
		digits := make([]int64, 0, length)
		for i := int64(0); i < length; i++ {
			var d int64
			if nextRandom(&seed)%2 == 0 {
				d = 9
			} else {
				d = nextRandom(&seed) % 10
			}
			if i == 0 && d == 0 {
				d = 1
			}
			digits = append(digits, d)
		}
		var head *ListNode
		for i := length - 1; i >= 0; i-- {
			head = &ListNode{Val: digits[i], Next: head}
		}
		numbers = append(numbers, head)
	}
	totalDigits := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		for i := int64(0); i < count; i++ {
			for n := addTwoNumbers(numbers[i], numbers[(i+1)%count]); n != nil; n = n.Next {
				totalDigits++
				checksum = (checksum*31 + n.Val + round) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds on %d numbers: %d digits, checksum %d\n", rounds, count, totalDigits, checksum)
}
