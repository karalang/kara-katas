// Benchmark mirror of linked_list_random.kara (#382): reservoir sampling
// over a singly linked list.
package main

import "fmt"

type ListNode struct {
	val  int64
	next *ListNode
}

type Solution struct {
	head *ListNode
	seed int64
}

func (s *Solution) below(n int64) int64 {
	s.seed = (s.seed*1103515245 + 12345) % 2147483648
	return (s.seed / 65536) % n
}

func (s *Solution) getRandom() int64 {
	kept := int64(0)
	i := int64(0)
	for at := s.head; at != nil; at = at.next {
		i++
		if s.below(i) == 0 {
			kept = at.val
		}
	}
	return kept
}

func main() {
	seed := int64(7)
	var head *ListNode
	for k := 0; k < 10000; k++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		head = &ListNode{(seed/65536)%20001 - 10000, head}
	}
	s := &Solution{head, 382}
	checksum := int64(0)
	for q := 0; q < 20000; q++ {
		checksum = (checksum*31 + s.getRandom() + 10000) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
