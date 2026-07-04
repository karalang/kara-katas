// Benchmark workload — Spiral Matrix II (LeetCode #59).
// Go mirror of ../spiral_matrix_ii.kara. Same M=9 rotated sizes (n=12..20),
// K=180k, boundary-shrinking generator over a nested [][]int64, position-
// weighted checksum, and sink — see that file's header for the rationale.

package main

import "fmt"

func generateMatrix(n int64) [][]int64 {
	grid := make([][]int64, n)
	for r := int64(0); r < n; r++ {
		grid[r] = make([]int64, n)
	}

	top, bottom, left, right, v := int64(0), n-1, int64(0), n-1, int64(1)
	for top <= bottom && left <= right {
		for c := left; c <= right; c++ {
			grid[top][c] = v
			v++
		}
		top++

		for r2 := top; r2 <= bottom; r2++ {
			grid[r2][right] = v
			v++
		}
		right--

		if top <= bottom {
			for c2 := right; c2 >= left; c2-- {
				grid[bottom][c2] = v
				v++
			}
			bottom--
		}

		if left <= right {
			for r3 := bottom; r3 >= top; r3-- {
				grid[r3][left] = v
				v++
			}
			left++
		}
	}
	return grid
}

func checksum(grid [][]int64, n int64) int64 {
	var s int64 = 0
	for i := int64(0); i < n; i++ {
		for j := int64(0); j < n; j++ {
			s += grid[i][j] * (i*n + j + 1)
		}
	}
	return s
}

func main() {
	const mSizes int64 = 9
	const kIters int64 = 180000

	var total int64 = 0
	for k := int64(0); k < kIters; k++ {
		n := 12 + (k % mSizes)
		g := generateMatrix(n)
		total += checksum(g, n)
	}
	fmt.Println(total)
}
