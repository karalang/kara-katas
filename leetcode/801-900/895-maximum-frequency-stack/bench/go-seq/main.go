// Bench mirror for LeetCode #895 — same algorithm as the Kara version.
package main

import "fmt"

type FreqStack struct {
	freq    map[int64]int64
	buckets map[int64][]int64
	maxfreq int64
}

func newFreqStack() *FreqStack {
	return &FreqStack{freq: map[int64]int64{}, buckets: map[int64][]int64{}}
}

func (s *FreqStack) push(x int64) {
	f := s.freq[x] + 1
	s.freq[x] = f
	if f > s.maxfreq {
		s.maxfreq = f
	}
	b := s.buckets[f]
	b = append(b, x)
	s.buckets[f] = b
}

func (s *FreqStack) pop() int64 {
	top := s.maxfreq
	b := s.buckets[top]
	x := b[len(b)-1]
	b = b[:len(b)-1]
	drained := len(b) == 0
	s.buckets[top] = b
	s.freq[x] = s.freq[x] - 1
	if drained {
		s.maxfreq = top - 1
	}
	return x
}

func run(rounds, steps int64) int64 {
	var checksum int64
	for r := int64(0); r < rounds; r++ {
		st := newFreqStack()
		seed := 12345 + r
		var live int64
		for i := int64(0); i < steps; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			if i%3 == 2 && live > 0 {
				checksum += st.pop() * (i%7 + 1)
				live--
			} else {
				st.push(seed % 12)
				live++
			}
		}
		for live > 0 {
			checksum += st.pop()
			live--
		}
	}
	return checksum
}

func main() {
	fmt.Println(run(120, 3000))
}
