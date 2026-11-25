// LeetCode #1380 bench -- Go: the ★ arm: each row's least value and each
// column's greatest found in one pass, then every cell that is both.
package main

import (
	"fmt"
	"math"
)

func luckyNumbers(matrix [][]int32) []int32 {
	m, n := len(matrix), len(matrix[0])
	rowMin := make([]int32, m)
	colMax := make([]int32, n)
	for i := range rowMin {
		rowMin[i] = math.MaxInt32
	}
	for j := range colMax {
		colMax[j] = math.MinInt32
	}
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			rowMin[i] = min(rowMin[i], matrix[i][j])
			colMax[j] = max(colMax[j], matrix[i][j])
		}
	}
	var lucky []int32
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if matrix[i][j] == rowMin[i] && matrix[i][j] == colMax[j] {
				lucky = append(lucky, matrix[i][j])
			}
		}
	}
	return lucky
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20 matrices of 50 by 50 built once; then 20000 rounds, each swapping
	// two cells of one matrix and finding its lucky numbers (see the Kāra
	// bench)
	const n = int64(50)
	seed := int64(1380)
	grids := make([][][]int32, 0, 20)
	for g := 0; g < 20; g++ {
		grid := make([][]int32, n)
		for i := int64(0); i < n; i++ {
			grid[i] = make([]int32, n)
			for j := int64(0); j < n; j++ {
				grid[i][j] = int32(i*n + j + 1)
			}
		}
		for s := 0; s < 300; s++ {
			a := nextRandom(&seed) % (n * n)
			b := nextRandom(&seed) % (n * n)
			grid[a/n][a%n], grid[b/n][b%n] = grid[b/n][b%n], grid[a/n][a%n]
		}
		grids = append(grids, grid)
	}
	check := int64(0)
	for r := int64(0); r < 20000; r++ {
		grid := grids[check%20]
		a := (check / 20) % (n * n)
		b := (check/7 + r) % (n * n)
		grid[a/n][a%n], grid[b/n][b%n] = grid[b/n][b%n], grid[a/n][a%n]
		lucky := luckyNumbers(grid)
		got := int64(len(lucky))
		for _, v := range lucky {
			got = got*2503 + int64(v)
		}
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("20000 rounds over 20 matrices of 50 by 50: checksum %d\n", check)
}
