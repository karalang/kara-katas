// LeetCode #2336: Smallest Number in Infinite Set -- the bench, the ★ arm
// in Go: every number from `next` on still in the set, and the numbers
// below it that were added back kept, as Go has no ordered set, in a
// binary min-heap with a flag per number for membership.
package main

import "fmt"

type smallestInfiniteSet struct {
	next   int64
	heap   []int64
	member []bool
}

func (s *smallestInfiniteSet) popSmallest() int64 {
	if len(s.heap) > 0 {
		least := s.heap[0]
		last := s.heap[len(s.heap)-1]
		s.heap = s.heap[:len(s.heap)-1]
		n := len(s.heap)
		i := 0
		for {
			c := 2*i + 1
			if c >= n {
				break
			}
			if c+1 < n && s.heap[c+1] < s.heap[c] {
				c++
			}
			if s.heap[c] >= last {
				break
			}
			s.heap[i] = s.heap[c]
			i = c
		}
		if n > 0 {
			s.heap[i] = last
		}
		s.member[least] = false
		return least
	}
	s.next++
	return s.next - 1
}

func (s *smallestInfiniteSet) addBack(num int64) {
	if num < s.next && !s.member[num] {
		s.member[num] = true
		s.heap = append(s.heap, num)
		i := len(s.heap) - 1
		for i > 0 && s.heap[(i-1)/2] > num {
			s.heap[i] = s.heap[(i-1)/2]
			i = (i - 1) / 2
		}
		s.heap[i] = num
	}
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	const calls = 200000
	ops := make([]int64, calls)
	for i := int64(0); i < calls; i++ {
		r := scrambled(i)
		if r%3 == 0 {
			ops[i] = r/3%5000 + 1
		}
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		s := &smallestInfiniteSet{next: 1, member: make([]bool, calls+2)}
		for _, op := range ops {
			if op == 0 {
				check = (check*31 + s.popSmallest()) % 1000000007
			} else {
				s.addBack(op)
			}
		}
	}
	fmt.Printf("50 passes over 2*10^5 calls: checksum %d\n", check)
}
