// LeetCode #2 — iterative add_two_numbers, Go single-threaded mirror.
// Algorithmic peer of bench/iterative.{kara,rs,c}. Same N=100 nine-digit
// lists built once, K=500_000 iterations. Stdout sink: 8 * K = 4_000_000.
//
// Idiomatic Go: GC-managed pointer-linked nodes — no manual free, no Rc.
// Carries the same alloc-per-digit shape; Go's GC handles drop instead
// of recursive Rc-dec (Rust) or explicit walk-and-free (C).
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

func addTwoNumbers(a, b *ListNode) *ListNode {
	var dummy ListNode
	tail := &dummy
	var carry int64
	for a != nil || b != nil || carry != 0 {
		s := carry
		if a != nil {
			s += a.val
			a = a.next
		}
		if b != nil {
			s += b.val
			b = b.next
		}
		tail.next = &ListNode{val: s % 10}
		tail = tail.next
		carry = s / 10
	}
	return dummy.next
}

func fromArray(arr []int64) *ListNode {
	if len(arr) == 0 {
		return nil
	}
	head := &ListNode{val: arr[0]}
	tail := head
	for _, v := range arr[1:] {
		tail.next = &ListNode{val: v}
		tail = tail.next
	}
	return head
}

func main() {
	const N = 100
	const K = 500_000
	a := make([]int64, N)
	b := make([]int64, N)
	for i := 0; i < N; i++ {
		a[i] = 9
		b[i] = 9
	}
	l1 := fromArray(a)
	l2 := fromArray(b)

	var sum int64
	for k := 0; k < K; k++ {
		out := addTwoNumbers(l1, l2)
		if out != nil {
			sum += out.val
		}
	}
	fmt.Println(sum)
}
