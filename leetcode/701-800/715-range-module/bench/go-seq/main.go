// LeetCode #715: Range Module -- a sorted list of disjoint ranges.
// Benchmark mirror of the Kara star arm: parallel sorted slices of
// starts and ends, a binary search on the ends, and inserts and removals
// that shift the rest.
package main

import "fmt"

type RangeModule struct {
	starts, ends []int64
}

func insertAt(s []int64, i int, v int64) []int64 {
	s = append(s, 0)
	copy(s[i+1:], s[i:])
	s[i] = v
	return s
}

func removeAt(s []int64, i int) []int64 {
	copy(s[i:], s[i+1:])
	return s[:len(s)-1]
}

func (m *RangeModule) firstEndingAfter(x int64) int {
	lo, hi := 0, len(m.ends)
	for lo < hi {
		mid := (lo + hi) / 2
		if m.ends[mid] > x {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func (m *RangeModule) addRange(left, right int64) {
	i := m.firstEndingAfter(left - 1)
	lo, hi, j := left, right, i
	for j < len(m.starts) && m.starts[j] <= right {
		if m.starts[j] < lo {
			lo = m.starts[j]
		}
		if m.ends[j] > hi {
			hi = m.ends[j]
		}
		j++
	}
	if j == i {
		m.starts = insertAt(m.starts, i, lo)
		m.ends = insertAt(m.ends, i, hi)
	} else {
		m.starts[i] = lo
		m.ends[i] = hi
		for k := i + 1; k < j; k++ {
			m.starts = removeAt(m.starts, i+1)
			m.ends = removeAt(m.ends, i+1)
		}
	}
}

func (m *RangeModule) queryRange(left, right int64) bool {
	i := m.firstEndingAfter(left)
	return i < len(m.starts) && m.starts[i] <= left && m.ends[i] >= right
}

func (m *RangeModule) removeRange(left, right int64) {
	i := m.firstEndingAfter(left)
	if i < len(m.starts) && m.starts[i] < left {
		end := m.ends[i]
		m.ends[i] = left
		if end > right {
			m.starts = insertAt(m.starts, i+1, right)
			m.ends = insertAt(m.ends, i+1, end)
			return
		}
		i++
	}
	for i < len(m.starts) && m.starts[i] < right {
		if m.ends[i] > right {
			m.starts[i] = right
			return
		}
		m.starts = removeAt(m.starts, i)
		m.ends = removeAt(m.ends, i)
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomBelow(seed *int64, bound int64) int64 {
	hi := nextRandom(seed)
	lo := nextRandom(seed)
	return (hi*32768 + lo) % bound
}

type call struct{ kind, left, right int64 }

func main() {
	seed := int64(715)
	var lists [][]call
	for l := 0; l < 10; l++ {
		calls := make([]call, 0, 100000)
		for c := 0; c < 100000; c++ {
			kind := nextRandom(&seed) % 3
			left := 1 + randomBelow(&seed, 10000000)
			right := left + 1 + randomBelow(&seed, 10000)
			calls = append(calls, call{kind, left, right})
		}
		lists = append(lists, calls)
	}
	held := 0
	for round := 0; round < 10; round++ {
		for _, calls := range lists {
			m := &RangeModule{}
			for _, c := range calls {
				if c.kind == 0 {
					m.addRange(c.left, c.right)
				} else if c.kind == 1 {
					m.removeRange(c.left, c.right)
				} else if m.queryRange(c.left, c.right) {
					held++
				}
			}
		}
	}
	fmt.Printf("10 rounds of 10 lists of 100000 calls: %d queries held\n", held)
}
