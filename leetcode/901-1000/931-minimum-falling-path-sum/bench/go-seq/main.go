// LeetCode #931: Minimum Falling Path Sum -- bench: one row of sums at a
// time. Mirrors min_falling_path_sum.kara.
package main

import "fmt"

func minFallingPathSum(matrix [][]int64) int64 {
	n := len(matrix)
	prev := make([]int64, n)
	copy(prev, matrix[0])
	for r := 1; r < n; r++ {
		cur := make([]int64, n)
		for c := 0; c < n; c++ {
			best := prev[c]
			if c > 0 && prev[c-1] < best {
				best = prev[c-1]
			}
			if c+1 < n && prev[c+1] < best {
				best = prev[c+1]
			}
			cur[c] = matrix[r][c] + best
		}
		prev = cur
	}
	answer := prev[0]
	for _, v := range prev {
		if v < answer {
			answer = v
		}
	}
	return answer
}

var seed int64 = 931

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 150, 100, 100
	// count matrices of n x n values from -100 to 100, built once
	matrices := make([][][]int64, count)
	for g := range matrices {
		matrix := make([][]int64, n)
		for i := range matrix {
			row := make([]int64, n)
			for j := range row {
				row[j] = nextRandom()%201 - 100
			}
			matrix[i] = row
		}
		matrices[g] = matrix
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every matrix, starting from a different one
		for i := 0; i < count; i++ {
			a := minFallingPathSum(matrices[(r+i)%count])
			total += a
			check = (check*1000003 + a + 1000000) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d matrices of %d x %d: answers summing to %d, checksum %d\n", rounds, count, n, n, total, check)
}
