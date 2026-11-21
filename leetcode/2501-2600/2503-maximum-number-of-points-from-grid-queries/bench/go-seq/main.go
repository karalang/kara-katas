// LeetCode #2503: Maximum Number of Points From Grid Queries -- Go mirror
// of the benchmark (points.kara): the same grids, queries, passes and
// checksum; the border in a hand-written binary min-heap of (value,
// cell), the queries' order by sort.SliceStable.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 2503

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(top int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % top
}

type entry struct{ value, cell int64 }

func less(a, b entry) bool { return a.value < b.value || (a.value == b.value && a.cell < b.cell) }

type minHeap []entry

func (h *minHeap) push(e entry) {
	*h = append(*h, e)
	s := *h
	i := len(s) - 1
	for i > 0 {
		up := (i - 1) / 2
		if !less(e, s[up]) {
			break
		}
		s[i] = s[up]
		i = up
	}
	s[i] = e
}

func (h *minHeap) pop() entry {
	s := *h
	top := s[0]
	last := s[len(s)-1]
	s = s[:len(s)-1]
	i := 0
	for {
		child := 2*i + 1
		if child >= len(s) {
			break
		}
		if child+1 < len(s) && less(s[child+1], s[child]) {
			child++
		}
		if !less(s[child], last) {
			break
		}
		s[i] = s[child]
		i = child
	}
	if len(s) > 0 {
		s[i] = last
	}
	*h = s
	return top
}

func maxPoints(grid [][]int64, queries []int64) []int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	order := make([]int, len(queries))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return queries[order[a]] < queries[order[b]] })
	answer := make([]int64, len(queries))
	seen := make([][]bool, m)
	for r := range seen {
		seen[r] = make([]bool, n)
	}
	border := &minHeap{}
	border.push(entry{grid[0][0], 0})
	seen[0][0] = true
	var reached int64
	dirs := [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for _, i := range order {
		q := queries[i]
		for len(*border) > 0 && (*border)[0].value < q {
			e := border.pop()
			reached++
			r, c := e.cell/n, e.cell%n
			for _, d := range dirs {
				rr, cc := r+d[0], c+d[1]
				if rr >= 0 && rr < m && cc >= 0 && cc < n && !seen[rr][cc] {
					seen[rr][cc] = true
					border.push(entry{grid[rr][cc], rr*n + cc})
				}
			}
		}
		answer[i] = reached
	}
	return answer
}

func main() {
	const passes = 14
	grids := make([][][]int64, 4)
	for g := range grids {
		grids[g] = make([][]int64, 316)
		for r := range grids[g] {
			grids[g][r] = make([]int64, 316)
			for c := range grids[g][r] {
				grids[g][r][c] = below(1000000) + 1
			}
		}
	}
	queries := make([]int64, 10000)
	for i := range queries {
		queries[i] = below(1000000) + 1
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		for g := 0; g < 4; g++ {
			r, c := check%316, check/316%316
			was := grids[g][r][c]
			grids[g][r][c] = (check+p)%1000000 + 1
			for _, a := range maxPoints(grids[g], queries) {
				check = (check*31 + a + p) % 1000000007
			}
			grids[g][r][c] = was
		}
	}
	fmt.Printf("%d passes over 4 grids of 316 by 316, 10^4 queries: checksum %d\n", passes, check)
}
