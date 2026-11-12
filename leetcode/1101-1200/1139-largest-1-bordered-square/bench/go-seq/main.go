// LeetCode #1139: Largest 1-Bordered Square -- the bench, the ★ arm's
// algorithm: runs of 1s left and up, each corner's sides tried from the longest down.
package main

import "fmt"

func largest1BorderedSquare(grid [][]int64) int64 {
	rows, cols := len(grid), len(grid[0])
	left := make([][]int64, rows)
	up := make([][]int64, rows)
	for i := range left {
		left[i] = make([]int64, cols)
		up[i] = make([]int64, cols)
	}
	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			if grid[i][j] == 1 {
				if j > 0 {
					left[i][j] = left[i][j-1] + 1
				} else {
					left[i][j] = 1
				}
				if i > 0 {
					up[i][j] = up[i-1][j] + 1
				} else {
					up[i][j] = 1
				}
			}
		}
	}
	var best int64
	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			k := min(left[i][j], up[i][j])
			for k > best {
				if left[int64(i)-k+1][j] >= k && up[i][int64(j)-k+1] >= k {
					best = k
				}
				k--
			}
		}
	}
	return best * best
}

var seed int64 = 1139

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	grids := make([][][]int64, 20)
	for g := range grids {
		grids[g] = make([][]int64, 100)
		for i := range grids[g] {
			row := make([]int64, 100)
			for j := range row {
				if nextRandom()%100 < 95 {
					row[j] = 1
				}
			}
			grids[g][i] = row
		}
	}
	var total, check int64
	for r := 0; r < 300; r++ {
		for g := 0; g < 20; g++ {
			i := nextRandom() % 100
			j := nextRandom() % 100
			grids[g][i][j] = 1 - grids[g][i][j]
			area := largest1BorderedSquare(grids[g])
			total += area
			check = (check*131 + area + 1) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 20 grids of 100 by 100: areas total %d, checksum %d\n", total, check)
}
