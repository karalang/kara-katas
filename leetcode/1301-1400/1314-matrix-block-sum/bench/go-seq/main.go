// LeetCode #1314 bench, Go: the ★ arm (a table of sums over every top-left
// rectangle, each block's sum four lookups) on the same 20 matrices and 200
// passes.
package main

import "fmt"

func matrixBlockSum(mat [][]int64, k int64) [][]int64 {
	m, n := int64(len(mat)), int64(len(mat[0]))
	sums := make([][]int64, m+1)
	for i := range sums {
		sums[i] = make([]int64, n+1)
	}
	for i := int64(0); i < m; i++ {
		for j := int64(0); j < n; j++ {
			sums[i+1][j+1] = mat[i][j] + sums[i][j+1] + sums[i+1][j] - sums[i][j]
		}
	}
	out := make([][]int64, m)
	for i := int64(0); i < m; i++ {
		out[i] = make([]int64, n)
		top, bottom := max(i-k, 0), min(i+k+1, m)
		for j := int64(0); j < n; j++ {
			left, right := max(j-k, 0), min(j+k+1, n)
			out[i][j] = sums[bottom][right] - sums[top][right] - sums[bottom][left] + sums[top][left]
		}
	}
	return out
}

var seed int64 = 1314

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100
	mats := make([][][]int64, 20)
	for g := range mats {
		mat := make([][]int64, n)
		for i := range mat {
			row := make([]int64, n)
			for j := range row {
				row[j] = 1 + nextRandom()%100
			}
			mat[i] = row
		}
		mats[g] = mat
	}
	var check int64
	for pass := int64(0); pass < 200; pass++ {
		for g := 0; g < 20; g++ {
			mats[g][check%n][(check/7)%n] = 1 + (check/11)%100
			var k int64
			if check%4 == 0 {
				k = 1 + (check/13)%100
			} else {
				k = 1 + (check/13)%5
			}
			got := matrixBlockSum(mats[g], k)
			check = (check*31 + got[(check/3)%n][(check/17)%n]) % 1000000007
			check = (check*31 + got[(check/19)%n][(check/23)%n] + pass) % 1000000007
		}
	}
	fmt.Printf("200 passes over 20 matrices of 100 by 100: checksum %d\n", check)
}
