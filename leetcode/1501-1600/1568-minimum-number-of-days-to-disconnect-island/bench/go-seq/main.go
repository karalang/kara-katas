// LeetCode #1568: Minimum Number of Days to Disconnect Island -- bench:
// the ★ arm (each land cell taken away in turn) over 20 grids of 30 by 30,
// built once, all land but for a water cell one time in 20; 5 passes, each
// first turning one cell of every grid over.
package main

import "fmt"

type cell struct{ r, c int64 }

func islands(grid [][]int64) int64 {
	rows := int64(len(grid))
	cols := int64(len(grid[0]))
	seen := make([][]bool, rows)
	for i := range seen {
		seen[i] = make([]bool, cols)
	}
	dirs := [4][2]int64{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	var count int64
	for r := int64(0); r < rows; r++ {
		for c := int64(0); c < cols; c++ {
			if grid[r][c] == 1 && !seen[r][c] {
				count++
				seen[r][c] = true
				stack := []cell{{r, c}}
				for len(stack) > 0 {
					at := stack[len(stack)-1]
					stack = stack[:len(stack)-1]
					for _, d := range dirs {
						a, b := at.r+d[0], at.c+d[1]
						if a >= 0 && a < rows && b >= 0 && b < cols && grid[a][b] == 1 && !seen[a][b] {
							seen[a][b] = true
							stack = append(stack, cell{a, b})
						}
					}
				}
			}
		}
	}
	return count
}

func minDays(source [][]int64) int64 {
	if islands(source) != 1 {
		return 0
	}
	grid := make([][]int64, len(source))
	for i, row := range source {
		grid[i] = append([]int64(nil), row...)
	}
	for r := range grid {
		for c := range grid[0] {
			if grid[r][c] == 1 {
				grid[r][c] = 0
				split := islands(grid) != 1
				grid[r][c] = 1
				if split {
					return 1
				}
			}
		}
	}
	return 2
}

var seed int64 = 1568

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 30
	const passes = 5
	grids := make([][][]int64, 0, 20)
	for g := 0; g < 20; g++ {
		grid := make([][]int64, 0, n)
		for r := 0; r < n; r++ {
			row := make([]int64, 0, n)
			for c := 0; c < n; c++ {
				if nextRandom()%20 == 0 {
					row = append(row, 0)
				} else {
					row = append(row, 1)
				}
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	var check int64
	var days [3]int64
	for p := int64(0); p < passes; p++ {
		for g := range grids {
			at := (p*7919 + int64(g)*104729) % (n * n)
			grids[g][at/n][at%n] = 1 - grids[g][at/n][at%n]
			answer := minDays(grids[g])
			days[answer]++
			check = mix(check, answer)
		}
	}
	fmt.Printf("%d passes over 20 grids of 30 by 30: %d need 0 days, %d need 1, %d need 2, checksum %d\n",
		passes, days[0], days[1], days[2], check)
}
