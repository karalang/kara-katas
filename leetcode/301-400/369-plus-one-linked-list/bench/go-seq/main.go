// Benchmark for #369 -- mirror of plus_one.kara.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func plusOne(head *ListNode) *ListNode {
	front := &ListNode{0, head}
	last := front
	for at := front.next; at != nil; at = at.next {
		if at.val != 9 {
			last = at
		}
	}
	last.val++
	for rest := last.next; rest != nil; rest = rest.next {
		rest.val = 0
	}
	if front.val == 1 {
		return front
	}
	return front.next
}

func main() {
	var seed int64 = 369
	var total, checksum int64
	for i := 0; i < 20; i++ {
		var head *ListNode
		for k := 0; k < 100000; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			var d int64
			if i%2 == 0 && k < 50000 {
				d = 9
			} else {
				d = (seed / 65536) % 10
			}
			if k == 99999 && d == 0 {
				d = 1
			}
			head = &ListNode{d, head}
		}
		for r := 0; r < 20; r++ {
			head = plusOne(head)
		}
		for at := head; at != nil; at = at.next {
			total++
			checksum = (checksum*31 + at.val) % 1000000007
		}
	}
	fmt.Printf("%d digits, checksum %d\n", total, checksum)
}
