// Benchmark workload for LeetCode #328 — Go mirror of odd_even_list.kara.
//
// Same workload: a list of LEN nodes built once, then PUNCHES punches, each
// regrouping the list in place and walking it once to fold a rolling hash
// and replace one value.
package main

import "fmt"

const (
	LEN     = 1000000
	PUNCHES = 10
	MODULUS = 1073741789
)

type ListNode struct {
	val  int64
	next *ListNode
}

func oddEvenList(head *ListNode) *ListNode {
	if head == nil || head.next == nil {
		return head
	}
	first, second := head, head.next
	odd, even := first, second
	for {
		n := even.next
		if n == nil {
			break
		}
		odd.next = n
		odd = n
		even.next = n.next
		if n.next == nil {
			break
		}
		even = n.next
	}
	odd.next = second
	return first
}

var seed int64 = 328

func nextRand() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var head *ListNode
	for i := 0; i < LEN; i++ {
		hi := nextRand()
		lo := nextRand()
		head = &ListNode{val: (hi*32768 + lo) % 1000000, next: head}
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		head = oddEvenList(head)
		hi := nextRand()
		lo := nextRand()
		pos := (hi*32768 + lo) % LEN
		hi = nextRand()
		lo = nextRand()
		fresh := (hi*32768 + lo) % 1000000
		var k int64
		for n := head; n != nil; n = n.next {
			if k == pos {
				n.val = fresh
			}
			sink = (sink*31 + n.val*(k+1)) % MODULUS
			k++
		}
	}
	fmt.Printf("sink %d\n", sink)
}
