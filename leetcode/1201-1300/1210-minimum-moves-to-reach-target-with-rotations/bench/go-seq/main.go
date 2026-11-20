// LeetCode #1210 bench, in Go: the ★ arm (a breadth-first search over the
// snake's states, its tail cell and whether it lies flat or upright) on 24
// grids of 100 by 100 drawn once, then 40 rounds over the grids, every
// answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1210

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type state struct{ r, c, up int64 }

func minimumMoves(grid [][]int64) int64 {
	n := int64(len(grid))
	free := func(r, c int64) bool { return r < n && c < n && grid[r][c] == 0 }
	dist := make([]int64, n*n*2)
	for i := range dist {
		dist[i] = -1
	}
	queue := []state{{0, 0, 0}}
	dist[0] = 0
	for head := 0; head < len(queue); head++ {
		s := queue[head]
		r, c, up := s.r, s.c, s.up
		d := dist[(r*n+c)*2+up]
		if r == n-1 && c == n-2 && up == 0 {
			return d
		}
		next := make([]state, 0, 3)
		if up == 0 {
			if free(r, c+2) {
				next = append(next, state{r, c + 1, 0})
			}
			if free(r+1, c) && free(r+1, c+1) {
				next = append(next, state{r + 1, c, 0}, state{r, c, 1})
			}
		} else {
			if free(r+2, c) {
				next = append(next, state{r + 1, c, 1})
			}
			if free(r, c+1) && free(r+1, c+1) {
				next = append(next, state{r, c + 1, 1}, state{r, c, 0})
			}
		}
		for _, t := range next {
			at := (t.r*n+t.c)*2 + t.up
			if dist[at] < 0 {
				dist[at] = d + 1
				queue = append(queue, t)
			}
		}
	}
	return -1
}

func randomGrid(n, percent int64) [][]int64 {
	grid := make([][]int64, n)
	for r := int64(0); r < n; r++ {
		grid[r] = make([]int64, n)
		for c := int64(0); c < n; c++ {
			corner := (r == 0 && c < 2) || (r == n-1 && c >= n-2)
			if !corner && nextRandom()%100 < percent {
				grid[r][c] = 1
			}
		}
	}
	return grid
}

func staircase(n, s int64) [][]int64 {
	grid := make([][]int64, n)
	for r := range grid {
		grid[r] = make([]int64, n)
		for c := range grid[r] {
			grid[r][c] = 1
		}
	}
	open := func(r, c int64) {
		if r < n && c < n {
			grid[r][c] = 0
		}
	}
	for k := int64(0); k*s < n; k++ {
		at := k * s
		for c := at; c < at+s+2; c++ {
			open(at, c)
		}
		for r := at; r < at+s+2; r++ {
			open(r, at+s)
		}
		for d := int64(0); d < 4; d++ {
			open(at+d/2, at+d%2)
			open(at+d/2, at+s+d%2)
		}
	}
	for i := int64(0); i < n; i++ {
		open(n-1, i)
		open(n-2, i)
		open(i, n-1)
		open(i, n-2)
	}
	return grid
}

func main() {
	grids := [][][]int64{}
	for i := 0; i < 20; i++ {
		percent := int64(14)
		if i < 8 {
			percent = 5
		} else if i < 16 {
			percent = 10
		}
		grids = append(grids, randomGrid(100, percent))
	}
	for s := int64(3); s < 7; s++ {
		grids = append(grids, staircase(100, s))
	}
	var check int64
	for round := int64(0); round < 40; round++ {
		for _, g := range grids {
			check = (check*131 + minimumMoves(g) + 2 + round) % 1000000007
		}
	}
	fmt.Printf("40 rounds over 24 grids of 100 by 100: checksum %d\n", check)
}
