// Benchmark: LeetCode #994 Rotting Oranges -- the ★ arm, a
// breadth-first search from every rotten orange at once, on random grids
// of 10 by 10, LeetCode's largest. Mirrors oranges_rotting.kara, .c, .rs
// and .py.
package main

import "fmt"

type cell struct{ r, c, t int64 }

var steps = [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}

func orangesRotting(grid [][]int64) int64 {
	m := int64(len(grid))
	n := int64(len(grid[0]))
	g := make([][]int64, m)
	for r := range g {
		g[r] = append([]int64(nil), grid[r]...)
	}
	var queue []cell
	var fresh int64
	for r := int64(0); r < m; r++ {
		for c := int64(0); c < n; c++ {
			if g[r][c] == 2 {
				queue = append(queue, cell{r, c, 0})
			} else if g[r][c] == 1 {
				fresh++
			}
		}
	}
	var minutes int64
	for head := 0; head < len(queue); head++ {
		x := queue[head]
		minutes = x.t
		for _, s := range steps {
			nr, nc := x.r+s[0], x.c+s[1]
			if nr >= 0 && nr < m && nc >= 0 && nc < n && g[nr][nc] == 1 {
				g[nr][nc] = 2
				fresh--
				queue = append(queue, cell{nr, nc, x.t + 1})
			}
		}
	}
	if fresh > 0 {
		return -1
	}
	return minutes
}

var seed int64 = 994

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomGrid() [][]int64 {
	grid := make([][]int64, 10)
	for r := range grid {
		grid[r] = make([]int64, 10)
		for c := range grid[r] {
			k := nextRandom() % 32
			if k < 3 {
				grid[r][c] = 0
			} else if k == 3 {
				grid[r][c] = 2
			} else {
				grid[r][c] = 1
			}
		}
	}
	return grid
}

func main() {
	rounds := 20000
	grids := make([][][]int64, 20)
	for i := range grids {
		grids[i] = randomGrid()
	}
	var stuck, total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			got := orangesRotting(grids[(r+i)%20])
			if got < 0 {
				stuck++
			} else {
				total += got
			}
			check = (check*31 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 grids of 10 by 10: %d never rot, %d minutes, checksum %d\n", rounds, stuck, total, check)
}
