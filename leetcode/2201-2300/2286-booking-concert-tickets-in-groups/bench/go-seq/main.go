// LeetCode #2286: Booking Concert Tickets in Groups -- the bench, the ★
// arm's Go twin. A segment tree of each range's largest free run and
// free total.
package main

import "fmt"

type BookMyShow struct {
	seats, size int64
	most, free  []int64
}

func newShow(n, m int64) *BookMyShow {
	size := int64(1)
	for size < n {
		size *= 2
	}
	s := &BookMyShow{seats: m, size: size, most: make([]int64, 2*size), free: make([]int64, 2*size)}
	for r := int64(0); r < n; r++ {
		s.most[size+r] = m
		s.free[size+r] = m
	}
	for p := size - 1; p >= 1; p-- {
		s.most[p] = max(s.most[2*p], s.most[2*p+1])
		s.free[p] = s.free[2*p] + s.free[2*p+1]
	}
	return s
}

func (s *BookMyShow) set(row, left int64) {
	p := s.size + row
	s.most[p] = left
	s.free[p] = left
	for p /= 2; p >= 1; p /= 2 {
		s.most[p] = max(s.most[2*p], s.most[2*p+1])
		s.free[p] = s.free[2*p] + s.free[2*p+1]
	}
}

func (s *BookMyShow) leftmost(k int64) int64 {
	if s.most[1] < k {
		return -1
	}
	p := int64(1)
	for p < s.size {
		if s.most[2*p] >= k {
			p = 2 * p
		} else {
			p = 2*p + 1
		}
	}
	return p - s.size
}

func (s *BookMyShow) freeThrough(row int64) int64 {
	var total int64
	lo, hi := s.size, s.size+row+1
	for lo < hi {
		if lo%2 == 1 {
			total += s.free[lo]
			lo++
		}
		if hi%2 == 1 {
			hi--
			total += s.free[hi]
		}
		lo /= 2
		hi /= 2
	}
	return total
}

func (s *BookMyShow) gather(k, maxRow int64) []int64 {
	row := s.leftmost(k)
	if row < 0 || row > maxRow {
		return nil
	}
	left := s.free[s.size+row]
	s.set(row, left-k)
	return []int64{row, s.seats - left}
}

func (s *BookMyShow) scatter(k, maxRow int64) bool {
	if s.freeThrough(maxRow) < k {
		return false
	}
	need := k
	for need > 0 {
		row := s.leftmost(1)
		left := s.free[s.size+row]
		take := min(left, need)
		s.set(row, left-take)
		need -= take
	}
	return true
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2286

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

type call struct {
	gather    bool
	k, maxRow int64
}

func main() {
	calls := make([]call, 0, 50000)
	for i := 0; i < 50000; i++ {
		k := wideRandom()%1000000000 + 1
		maxRow := wideRandom() % 50000
		calls = append(calls, call{nextRandom()%2 == 0, k, maxRow})
	}
	var check int64
	for t := 0; t < 40; t++ {
		show := newShow(50000, 1000000000)
		for _, c := range calls {
			var mark int64
			if c.gather {
				got := show.gather(c.k, c.maxRow)
				if len(got) == 2 {
					mark = (got[0]*1000003+got[1])%1000000007 + 3
				}
			} else if show.scatter(c.k, c.maxRow) {
				mark = 1
			} else {
				mark = 2
			}
			check = (check*31 + mark) % 1000000007
		}
	}
	fmt.Printf("40 shows of 50000 calls: checksum %d\n", check)
}
