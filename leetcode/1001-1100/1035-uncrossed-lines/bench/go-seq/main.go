// LeetCode #1035: Uncrossed Lines -- bench
// Mirrors ../uncrossed_lines.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func maxUncrossedLines(nums1, nums2 []int64) int64 {
	m, n := len(nums1), len(nums2)
	best := make([][]int64, m+1)
	for i := range best {
		best[i] = make([]int64, n+1)
	}
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if nums1[i-1] == nums2[j-1] {
				best[i][j] = best[i-1][j-1] + 1
			} else {
				best[i][j] = max(best[i-1][j], best[i][j-1])
			}
		}
	}
	return best[m][n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count, rounds := 40, 20
	seed := int64(1035)
	type pair struct{ a, b []int64 }
	pairs := []pair{}
	for p := 0; p < count; p++ {
		a := make([]int64, 500)
		b := make([]int64, 500)
		for i := range a {
			a[i] = nextRandom(&seed)%10 + 1
		}
		for i := range b {
			b[i] = nextRandom(&seed)%10 + 1
		}
		pairs = append(pairs, pair{a, b})
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, p := range pairs {
			lines := maxUncrossedLines(p.a, p.b)
			total += lines
			check = (check*131 + lines) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 500 values, %d rounds: sum %d, checksum %d\n", count, rounds, total, check)
}
