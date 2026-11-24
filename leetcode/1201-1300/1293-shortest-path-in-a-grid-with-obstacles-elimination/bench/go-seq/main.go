// LeetCode #1293 bench: the ★ arm over 50 grids of 40 by 40 with obstacles 30
// in 100, built once; then 80 passes, each flipping one cell of every grid and
// choosing k from the checksum so far, answering it. The queue is a slice
// with a head index, as a Go programmer writes a breadth-first queue.
package main

import "fmt"

type state struct{ r, c, left int64 }

func shortestPath(grid [][]int64, k int64) int64 {
	m, n := int64(len(grid)), int64(len(grid[0]))
	if k >= m+n-2 {
		return m + n - 2
	}
	best := make([][]int64, m)
	for i := range best {
		best[i] = make([]int64, n)
		for j := range best[i] {
			best[i][j] = -1
		}
	}
	queue := []state{{0, 0, k}}
	best[0][0] = k
	dirs := [4][2]int64{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	var steps int64
	for len(queue) > 0 {
		level := queue
		queue = nil
		for _, s := range level {
			if s.r == m-1 && s.c == n-1 {
				return steps
			}
			for _, d := range dirs {
				nr, nc := s.r+d[0], s.c+d[1]
				if nr < 0 || nr >= m || nc < 0 || nc >= n {
					continue
				}
				rest := s.left - grid[nr][nc]
				if rest > best[nr][nc] {
					best[nr][nc] = rest
					queue = append(queue, state{nr, nc, rest})
				}
			}
		}
		steps++
	}
	return -1
}

func main() {
	seed := int64(1293)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	grids := make([][][]int64, 50)
	for a := range grids {
		grids[a] = make([][]int64, 40)
		for i := range grids[a] {
			grids[a][i] = make([]int64, 40)
			for j := range grids[a][i] {
				corner := (i == 0 && j == 0) || (i == 39 && j == 39)
				if !corner && nextRandom()%100 < 30 {
					grids[a][i][j] = 1
				}
			}
		}
	}
	var check int64
	for p := int64(0); p < 80; p++ {
		for a := range grids {
			cell := 1 + check%1598
			grids[a][cell/40][cell%40] = 1 - grids[a][cell/40][cell%40]
			check = (check*31 + shortestPath(grids[a], check%78) + 2 + p) % 1000000007
		}
	}
	fmt.Printf("80 passes over 50 grids of 40 by 40: checksum %d\n", check)
}
