package main

import "fmt"

func main() {
	var n, passes int64 = 50000, 250

	val := make([]int64, n)
	left := make([]int64, n)
	right := make([]int64, n)

	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		val[i] = state >> 16
		left[i] = -1
		right[i] = -1
	}

	for i := int64(1); i < n; i++ {
		cur := int64(0)
		placed := false
		for !placed {
			if val[i] < val[cur] {
				if left[cur] < 0 {
					left[cur] = i
					placed = true
				} else {
					cur = left[cur]
				}
			} else {
				if right[cur] < 0 {
					right[cur] = i
					placed = true
				} else {
					cur = right[cur]
				}
			}
		}
	}

	s1 := make([]int64, n)
	s2 := make([]int64, n)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := p % n
		val[idx]++

		s1p := int64(0)
		s1[s1p] = 0
		s1p++
		s2p := int64(0)
		for s1p > 0 {
			s1p--
			node := s1[s1p]
			s2[s2p] = node
			s2p++
			l := left[node]
			r := right[node]
			if l >= 0 {
				s1[s1p] = l
				s1p++
			}
			if r >= 0 {
				s1[s1p] = r
				s1p++
			}
		}
		var pos, acc int64 = 0, 0
		for s2p > 0 {
			s2p--
			node := s2[s2p]
			acc += val[node] * (pos + 1)
			pos++
		}
		sink += acc
	}
	fmt.Println(sink)
}
