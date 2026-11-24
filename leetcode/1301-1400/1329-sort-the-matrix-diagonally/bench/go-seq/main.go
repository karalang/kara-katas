// LeetCode #1329 bench, Go mirror of the Kāra bench: the ★ arm (each
// diagonal read into a slice, sorted with slices.Sort and written back) on
// 8 matrices of 300 by 300, values 1 to 100, built once. Then 100 passes,
// each setting one cell of every matrix from the checksum so far,
// answering it and folding two of the answer's cells plus the pass into
// the checksum.
package main

import (
	"fmt"
	"slices"
)

func sortFrom(out [][]int32, i0, j0 int) {
	m, n := len(out), len(out[0])
	var vals []int32
	for k := 0; i0+k < m && j0+k < n; k++ {
		vals = append(vals, out[i0+k][j0+k])
	}
	slices.Sort(vals)
	for k, v := range vals {
		out[i0+k][j0+k] = v
	}
}

func diagonalSort(mat [][]int32) [][]int32 {
	out := make([][]int32, len(mat))
	for i, row := range mat {
		out[i] = append([]int32(nil), row...)
	}
	for i := range mat {
		sortFrom(out, i, 0)
	}
	for j := 1; j < len(mat[0]); j++ {
		sortFrom(out, 0, j)
	}
	return out
}

var seed int64 = 1329

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const size = 300
	mats := make([][][]int32, 8)
	for t := range mats {
		mats[t] = make([][]int32, size)
		for i := range mats[t] {
			mats[t][i] = make([]int32, size)
			for j := range mats[t][i] {
				mats[t][i][j] = int32(1 + nextRandom()%100)
			}
		}
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		for t := 0; t < 8; t++ {
			r := check % size
			c := (check / 7) % size
			mats[t][r][c] = int32(1 + (check/13)%100)
			out := diagonalSort(mats[t])
			check = (check*31 + int64(out[r][c]) + int64(out[size-1][size/2]) + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 8 matrices of 300 by 300: checksum %d\n", check)
}
