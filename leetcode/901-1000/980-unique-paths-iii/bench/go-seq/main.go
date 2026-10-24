// Benchmark: LeetCode #980 Unique Paths III -- the ★ arm, backtracking
// on the grid, on every start and end of an open 4 x 5 grid, LeetCode's
// largest. Mirrors unique_paths_iii.kara, .rs, .c and .py.
package main

import "fmt"

func walk(grid [][]int64, r, c int, left int64) int64 {
	if r < 0 || c < 0 || r >= len(grid) || c >= len(grid[0]) || grid[r][c] == -1 {
		return 0
	}
	if grid[r][c] == 2 {
		if left == 0 {
			return 1
		}
		return 0
	}
	grid[r][c] = -1
	paths := walk(grid, r+1, c, left-1) + walk(grid, r-1, c, left-1) +
		walk(grid, r, c+1, left-1) + walk(grid, r, c-1, left-1)
	grid[r][c] = 0
	return paths
}

func uniquePathsIII(grid [][]int64) int64 {
	g := make([][]int64, len(grid))
	sr, sc := 0, 0
	var left int64
	for r := range grid {
		g[r] = append([]int64(nil), grid[r]...)
		for c := range grid[r] {
			if g[r][c] == 1 {
				sr, sc = r, c
			} else if g[r][c] != -1 {
				left++
			}
		}
	}
	g[sr][sc] = 0
	return walk(g, sr, sc, left)
}

func main() {
	rounds, rows, cols := 20, 4, 5
	var total, check int64
	for round := 0; round < rounds; round++ {
		for s := 0; s < rows*cols; s++ {
			for e := 0; e < rows*cols; e++ {
				if s == e {
					continue
				}
				grid := make([][]int64, rows)
				for r := range grid {
					grid[r] = make([]int64, cols)
				}
				grid[s/cols][s%cols] = 1
				grid[e/cols][e%cols] = 2
				p := uniquePathsIII(grid)
				total += p
				check = (check*31 + p + int64(s)) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 380 starts and ends of a 4 x 5 grid: %d paths, checksum %d\n", rounds, total, check)
}
