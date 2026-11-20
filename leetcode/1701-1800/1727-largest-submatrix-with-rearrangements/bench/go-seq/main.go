// LeetCode #1727: Largest Submatrix With Rearrangements -- the bench
// (submatrix.kara): each row's column heights sorted, the k-th from the
// shortest giving a submatrix n - k wide.
package main

import (
	"fmt"
	"sort"
)

func largestSubmatrix(matrix [][]int32) int32 {
	n := len(matrix[0])
	heights := make([]int32, n)
	sorted := make([]int32, n)
	var best int32
	for _, row := range matrix {
		for j := 0; j < n; j++ {
			if row[j] == 1 {
				heights[j]++
			} else {
				heights[j] = 0
			}
		}
		copy(sorted, heights)
		sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
		for k := 0; k < n; k++ {
			best = max(best, sorted[k]*int32(n-k))
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 20
	var rounds int64 = 50
	side := 316
	var seed int64 = 1727
	problems := make([][][]int32, count)
	for c := range problems {
		problems[c] = make([][]int32, side)
		for i := range problems[c] {
			row := make([]int32, side)
			for j := range row {
				if nextRandom(&seed)%8 != 0 {
					row[j] = 1
				}
			}
			problems[c][i] = row
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, matrix := range problems {
			answer := int64(largestSubmatrix(matrix))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d matrices of %d by %d, %d rounds: areas sum to %d, checksum %d\n", count, side, side, rounds, sum, check)
}
