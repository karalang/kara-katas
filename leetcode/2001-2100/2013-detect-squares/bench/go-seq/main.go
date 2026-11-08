// LeetCode #2013: Detect Squares -- the ★ arm's benchmark, a mirror of
// squares.kara.
package main

import "fmt"

type point struct{ x, y int64 }

type detectSquares struct {
	rows   [][]int64
	points []point
}

func newDetectSquares() *detectSquares {
	return &detectSquares{rows: make([][]int64, 1001)}
}

func (s *detectSquares) at(x, y int64) int64 {
	if len(s.rows[x]) == 0 {
		return 0
	}
	return s.rows[x][y]
}

func (s *detectSquares) add(p point) {
	if len(s.rows[p.x]) == 0 {
		s.rows[p.x] = make([]int64, 1001)
	}
	if s.rows[p.x][p.y] == 0 {
		s.points = append(s.points, p)
	}
	s.rows[p.x][p.y]++
}

func abs(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func (s *detectSquares) count(p point) int64 {
	var ways int64
	for _, q := range s.points {
		if q.x != p.x && abs(q.x-p.x) == abs(q.y-p.y) {
			ways += s.at(q.x, q.y) * s.at(p.x, q.y) * s.at(q.x, p.y)
		}
	}
	return ways
}

var seed int64 = 2013

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var calls, sum, check int64
	for r := int64(0); r < 20; r++ {
		s := newDetectSquares()
		for i := 0; i < 20000; i++ {
			base := (r % 10) * 90
			p := point{base + nextRandom()%60, 0}
			p.y = base + nextRandom()%60
			if nextRandom()%3 == 0 {
				ways := s.count(p)
				calls++
				sum += ways
				check = (check*31 + ways) % 1000000007
			} else {
				s.add(p)
			}
		}
	}
	fmt.Printf("%d counts: sum %d, checksum %d\n", calls, sum, check)
}
