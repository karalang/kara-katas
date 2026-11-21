// LeetCode #2435: Paths in Matrix Whose Sum Is Divisible by K -- the
// bench, the ★ arm: one row of counts by remainder, each cell's from
// above, still in place, and from the left, shifted by its value.
package main

import "fmt"

const mod = 1000000007

func numberOfPaths(grid [][]int64, k int64) int64 {
	n := len(grid[0])
	row := make([][]int64, n)
	for j := range row {
		row[j] = make([]int64, k)
	}
	for i := range grid {
		for j := 0; j < n; j++ {
			came := make([]int64, k)
			if i == 0 && j == 0 {
				came[0] = 1
			}
			for r := int64(0); r < k; r++ {
				var left int64
				if j > 0 {
					left = row[j-1][r]
				}
				came[r] = (came[r] + row[j][r] + left) % mod
			}
			v := grid[i][j]
			for r := int64(0); r < k; r++ {
				row[j][(r+v)%k] = came[r]
			}
		}
	}
	return row[n-1][0]
}

var seed int64 = 2435

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var grids [][][]int64
	for g := 0; g < 5; g++ {
		var grid [][]int64
		for i := 0; i < 200; i++ {
			var row []int64
			for j := 0; j < 250; j++ {
				row = append(row, nextRandom()%101)
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for g := range grids {
			grids[g][(p*37)%200][(p*91)%250] = p
			check = (check*31 + numberOfPaths(grids[g], 50) + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 5 grids of 200 by 250: checksum %d\n", check)
}
