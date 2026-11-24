// LeetCode #1292 bench: the ★ arm over 20 matrices of 300 by 300 with values
// up to 100, built once; then 100 passes, each setting one cell of every
// matrix and its threshold from the checksum so far and answering it.
package main

import "fmt"

func maxSideLength(mat [][]int64, threshold int64) int64 {
	m, n := len(mat), len(mat[0])
	sum := make([][]int64, m+1)
	for i := range sum {
		sum[i] = make([]int64, n+1)
	}
	best := 0
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			sum[i][j] = mat[i-1][j-1] + sum[i-1][j] + sum[i][j-1] - sum[i-1][j-1]
			k := best + 1
			if i >= k && j >= k && sum[i][j]-sum[i-k][j]-sum[i][j-k]+sum[i-k][j-k] <= threshold {
				best = k
			}
		}
	}
	return int64(best)
}

func main() {
	seed := int64(1292)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	mats := make([][][]int64, 20)
	for a := range mats {
		mats[a] = make([][]int64, 300)
		for i := range mats[a] {
			mats[a][i] = make([]int64, 300)
			for j := range mats[a][i] {
				mats[a][i][j] = nextRandom() % 101
			}
		}
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for a := range mats {
			mats[a][check%300][(check/300)%300] = check % 101
			threshold := check % 100001
			check = (check*31 + maxSideLength(mats[a], threshold) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 20 matrices of 300 by 300: checksum %d\n", check)
}
