// LeetCode #2711: Difference of Number of Distinct Values on Diagonals --
// the bench (diagonals.kara in Go): each diagonal swept down and then up
// with a table of the values seen.
package main

import "fmt"

func differenceOfDistinctValues(grid [][]int64) [][]int64 {
	m, n := len(grid), len(grid[0])
	answer := make([][]int64, m)
	for i := range answer {
		answer[i] = make([]int64, n)
	}
	type start struct{ r, c int }
	starts := make([]start, 0, m+n)
	for c := 0; c < n; c++ {
		starts = append(starts, start{0, c})
	}
	for r := 1; r < m; r++ {
		starts = append(starts, start{r, 0})
	}
	for _, s := range starts {
		length := m - s.r
		if n-s.c < length {
			length = n - s.c
		}
		var seen [51]bool
		var distinct int64
		for k := 0; k < length; k++ {
			answer[s.r+k][s.c+k] = distinct
			v := grid[s.r+k][s.c+k]
			if !seen[v] {
				seen[v] = true
				distinct++
			}
		}
		seen = [51]bool{}
		distinct = 0
		for k := length - 1; k >= 0; k-- {
			d := answer[s.r+k][s.c+k] - distinct
			if d < 0 {
				d = -d
			}
			answer[s.r+k][s.c+k] = d
			v := grid[s.r+k][s.c+k]
			if !seen[v] {
				seen[v] = true
				distinct++
			}
		}
	}
	return answer
}

var seed int64 = 2711

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 2000, 5
	grids := make([][][]int64, count)
	for g := range grids {
		cap := nextRandom()%50 + 1
		grids[g] = make([][]int64, 50)
		for r := range grids[g] {
			grids[g][r] = make([]int64, 50)
			for c := range grids[g][r] {
				grids[g][r][c] = nextRandom()%cap + 1
			}
		}
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, grid := range grids {
			for _, row := range differenceOfDistinctValues(grid) {
				for _, v := range row {
					sum += v
					check = (check*31 + v) % 1000000007
				}
			}
			check = (check + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d grids of 50 by 50, %d rounds: differences sum to %d, checksum %d\n", count, rounds, sum, check)
}
