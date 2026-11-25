// LeetCode #1388 bench -- Go: the ★ arm: the better of two straight runs,
// without the last slice and without the first; in each, best[i][j] is
// the most from at most j slices, no two adjacent, among the first i.
package main

import "fmt"

func bestInLine(slices []int32, n int) int32 {
	length := len(slices)
	best := make([][]int32, length+1)
	for i := range best {
		best[i] = make([]int32, n+1)
	}
	for i := 1; i <= length; i++ {
		for j := 1; j <= n; j++ {
			skip := best[i-1][j]
			take := slices[i-1]
			if i >= 2 {
				take += best[i-2][j-1]
			}
			best[i][j] = max(skip, take)
		}
	}
	return best[length][n]
}

func maxSizeSlices(slices []int32) int32 {
	n := len(slices) / 3
	length := len(slices)
	return max(bestInLine(slices[0:length-1], n), bestInLine(slices[1:length], n))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const length = 498
	seed := int64(1388)
	slices := make([]int32, length)
	for i := range slices {
		slices[i] = int32(1 + nextRandom(&seed)%1000)
	}
	check := int64(0)
	for round := 0; round < 1000; round++ {
		seed = (seed + check) % 2147483648
		at := nextRandom(&seed) % length
		slices[at] = int32(1 + nextRandom(&seed)%1000)
		check = (check*131 + int64(maxSizeSlices(slices))) % 1000000007
	}
	fmt.Printf("1000 rounds over 498 slices: checksum %d\n", check)
}
