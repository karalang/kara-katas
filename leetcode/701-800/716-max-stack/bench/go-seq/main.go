// LeetCode #716: Max Stack -- a stack of running maxima beside it.
// Benchmark mirror of the Kara star arm: each value with the largest
// value at or below it; popMax pops into a buffer until the max is on
// top, drops it, and pushes the buffer back.
package main

import "fmt"

type MaxStack struct {
	values, maxes []int64
}

func (s *MaxStack) push(x int64) {
	m := x
	if len(s.maxes) > 0 && s.maxes[len(s.maxes)-1] > x {
		m = s.maxes[len(s.maxes)-1]
	}
	s.values = append(s.values, x)
	s.maxes = append(s.maxes, m)
}

func (s *MaxStack) pop() int64 {
	s.maxes = s.maxes[:len(s.maxes)-1]
	x := s.values[len(s.values)-1]
	s.values = s.values[:len(s.values)-1]
	return x
}

func (s *MaxStack) top() int64 { return s.values[len(s.values)-1] }

func (s *MaxStack) peekMax() int64 { return s.maxes[len(s.maxes)-1] }

func (s *MaxStack) popMax() int64 {
	m := s.peekMax()
	var buffer []int64
	for s.top() != m {
		buffer = append(buffer, s.pop())
	}
	s.pop()
	for len(buffer) > 0 {
		x := buffer[len(buffer)-1]
		buffer = buffer[:len(buffer)-1]
		s.push(x)
	}
	return m
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type call struct{ kind, x int64 }

func main() {
	seed := int64(716)
	var lists [][]call
	for l := 0; l < 10; l++ {
		calls := make([]call, 0, 100000)
		size := 0
		for c := 0; c < 100000; c++ {
			if size == 0 || nextRandom(&seed)%2 == 0 {
				hi := nextRandom(&seed)
				lo := nextRandom(&seed)
				calls = append(calls, call{0, (hi*32768 + lo) % 1000001})
				size++
			} else {
				kind := 1 + nextRandom(&seed)%4
				calls = append(calls, call{kind, 0})
				if kind == 1 || kind == 4 {
					size--
				}
			}
		}
		lists = append(lists, calls)
	}
	sum := int64(0)
	for round := 0; round < 10; round++ {
		for _, calls := range lists {
			s := &MaxStack{}
			for _, c := range calls {
				switch c.kind {
				case 0:
					s.push(c.x)
				case 1:
					sum += s.pop()
				case 2:
					sum += s.top()
				case 3:
					sum += s.peekMax()
				default:
					sum += s.popMax()
				}
			}
		}
	}
	fmt.Printf("10 rounds of 10 lists of 100000 calls: sum %d\n", sum)
}
