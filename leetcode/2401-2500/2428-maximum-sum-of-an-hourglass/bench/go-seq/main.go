// LeetCode #2428: Maximum Sum of an Hourglass -- the bench, the ★ arm:
// every centre off the border, its seven cells added directly.
package main

import "fmt"

func maxSum(grid [][]int64) int64 {
	m, n := len(grid), len(grid[0])
	var best int64
	for r := 1; r < m-1; r++ {
		for c := 1; c < n-1; c++ {
			sum := grid[r-1][c-1] + grid[r-1][c] + grid[r-1][c+1] +
				grid[r][c] +
				grid[r+1][c-1] + grid[r+1][c] + grid[r+1][c+1]
			if sum > best {
				best = sum
			}
		}
	}
	return best
}

var seed int64 = 2428

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var grids [][][]int64
	for g := 0; g < 10; g++ {
		var grid [][]int64
		for r := 0; r < 150; r++ {
			var row []int64
			for c := 0; c < 150; c++ {
				a := nextRandom()
				row = append(row, (a*32768+nextRandom())%1000001)
			}
			grid = append(grid, row)
		}
		grids = append(grids, grid)
	}
	var check int64
	for p := int64(0); p < 600; p++ {
		for g := 0; g < 10; g++ {
			grids[g][(p*37)%150][(p*91)%150] = (p * 7919) % 1000001
			check = (check*31 + maxSum(grids[g]) + p) % 1000000007
		}
	}
	fmt.Printf("600 passes over 10 grids of 150 by 150: checksum %d\n", check)
}
