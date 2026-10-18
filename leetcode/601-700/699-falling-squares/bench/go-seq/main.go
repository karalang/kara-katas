// LeetCode #699: Falling Squares -- bench program, Go mirror of the segment-tree arm.
package main

import (
	"fmt"
	"slices"
	"sort"
)

var seed int64 = 699

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type tree struct {
	best, pending []int64
}

func (t *tree) pushDown(node int) {
	p := t.pending[node]
	if p >= 0 {
		for _, child := range [2]int{2 * node, 2*node + 1} {
			t.best[child] = p
			t.pending[child] = p
		}
		t.pending[node] = -1
	}
}

func (t *tree) query(node, lo, hi, from, to int) int64 {
	if to <= lo || hi <= from {
		return 0
	}
	if from <= lo && hi <= to {
		return t.best[node]
	}
	t.pushDown(node)
	mid := (lo + hi) / 2
	return max(t.query(2*node, lo, mid, from, to), t.query(2*node+1, mid, hi, from, to))
}

func (t *tree) set(node, lo, hi, from, to int, h int64) {
	if to <= lo || hi <= from {
		return
	}
	if from <= lo && hi <= to {
		t.best[node] = h
		t.pending[node] = h
		return
	}
	t.pushDown(node)
	mid := (lo + hi) / 2
	t.set(2*node, lo, mid, from, to, h)
	t.set(2*node+1, mid, hi, from, to, h)
	t.best[node] = max(t.best[2*node], t.best[2*node+1])
}

func fallingSquares(positions [][2]int64) []int64 {
	edges := []int64{}
	for _, p := range positions {
		edges = append(edges, p[0], p[0]+p[1])
	}
	slices.Sort(edges)
	edges = slices.Compact(edges)
	cells := len(edges)
	t := tree{best: make([]int64, 4*cells), pending: make([]int64, 4*cells)}
	for i := range t.pending {
		t.pending[i] = -1
	}
	answer := []int64{}
	for _, p := range positions {
		from := sort.Search(cells, func(i int) bool { return edges[i] >= p[0] })
		to := sort.Search(cells, func(i int) bool { return edges[i] >= p[0]+p[1] })
		top := t.query(1, 0, cells, from, to) + p[1]
		t.set(1, 0, cells, from, to, top)
		answer = append(answer, t.best[1])
	}
	return answer
}

func main() {
	problems := [][][2]int64{}
	for p := int64(0); p < 100; p++ {
		width := 1000 + p*999990
		biggest := 1 + nextRandom()%1000000
		positions := [][2]int64{}
		for i := 0; i < 1000; i++ {
			a := nextRandom()
			b := nextRandom()
			left := 1 + (a*32768+b)%width
			side := 1 + nextRandom()%biggest
			positions = append(positions, [2]int64{left, side})
		}
		problems = append(problems, positions)
	}
	rounds := 5
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for _, positions := range problems {
			heights := fallingSquares(positions)
			last := heights[len(heights)-1]
			total += last
			checksum = (checksum*31 + last) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 100 problems of 1000 squares: tallest stacks sum to %d, checksum %d\n", rounds, total, checksum)
}
