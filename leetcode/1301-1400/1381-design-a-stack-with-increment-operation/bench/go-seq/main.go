// LeetCode #1381 bench -- Go: the ★ arm: an increment is owed to the
// element k places up; a pop pays the top element what it is owed and
// hands the debt down to the one below.
package main

import "fmt"

type CustomStack struct {
	maxSize int
	stack   []int32
	owed    []int32
}

func newCustomStack(maxSize int) *CustomStack {
	return &CustomStack{maxSize: maxSize}
}

func (s *CustomStack) Push(x int32) {
	if len(s.stack) < s.maxSize {
		s.stack = append(s.stack, x)
		s.owed = append(s.owed, 0)
	}
}

func (s *CustomStack) Pop() int32 {
	n := len(s.stack)
	if n == 0 {
		return -1
	}
	x := s.stack[n-1]
	debt := s.owed[n-1]
	s.stack = s.stack[:n-1]
	s.owed = s.owed[:n-1]
	if n > 1 {
		s.owed[n-2] += debt
	}
	return x + debt
}

func (s *CustomStack) Increment(k int, val int32) {
	reach := min(len(s.stack), k)
	if reach > 0 {
		s.owed[reach-1] += val
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1381)
	check := int64(0)
	for round := 0; round < 2000; round++ {
		seed = (seed + check) % 2147483648
		s := newCustomStack(1000)
		for c := 0; c < 3000; c++ {
			r := nextRandom(&seed) % 10
			if r < 4 {
				s.Push(int32(1 + nextRandom(&seed)%1000))
			} else if r < 7 {
				k := 1 + nextRandom(&seed)%1000
				val := nextRandom(&seed) % 101
				s.Increment(int(k), int32(val))
			} else {
				check = (check*131 + int64(s.Pop()) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("2000 rounds of 3000 calls on a stack of 1000: checksum %d\n", check)
}
