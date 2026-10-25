// Benchmark: LeetCode #1000 Minimum Cost to Merge Stones -- the ★ arm,
// an interval table by length, on rows of up to 30 piles, LeetCode's
// largest. Mirrors merge_stones.kara, .c, .rs and .py.
package main

import "fmt"

func mergeStones(stones []int64, k int) int64 {
	n := len(stones)
	if (n-1)%(k-1) != 0 {
		return -1
	}
	prefix := make([]int64, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + stones[i]
	}
	dp := make([][]int64, n)
	for i := range dp {
		dp[i] = make([]int64, n)
	}
	for length := k; length <= n; length++ {
		for i := 0; i+length <= n; i++ {
			j := i + length - 1
			best := int64(1) << 60
			for m := i; m < j; m += k - 1 {
				if c := dp[i][m] + dp[m+1][j]; c < best {
					best = c
				}
			}
			if (length-1)%(k-1) == 0 {
				best += prefix[j+1] - prefix[i]
			}
			dp[i][j] = best
		}
	}
	return dp[0][n-1]
}

var seed int64 = 1000

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 5000
	// 20 rows, k from 2 to 11 twice over, each with as many piles of 1 to
	// 100 stones, up to 30, as k can merge down to one pile
	rows := make([][]int64, 20)
	ks := make([]int, 20)
	for t := 0; t < 20; t++ {
		k := 2 + t%10
		n := 1 + 29/(k-1)*(k-1)
		row := make([]int64, n)
		for i := range row {
			row[i] = 1 + nextRandom()%100
		}
		rows[t] = row
		ks[t] = k
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			t := (r + i) % 20
			got := mergeStones(rows[t], ks[t])
			total += got
			check = (check*31 + got + 2) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 rows of up to 30 piles: cost %d, checksum %d\n", rounds, total, check)
}
