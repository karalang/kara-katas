// LeetCode #1198 bench: the ★ arm in Go, over the same 20 matrices of
// 500 x 500 and 100 rounds as the Kāra bench.
package main

import "fmt"

func smallestCommonElement(mat [][]int64) int64 {
	var count [10001]int64
	for _, row := range mat {
		for _, v := range row {
			count[v]++
		}
	}
	for _, v := range mat[0] {
		if count[v] == int64(len(mat)) {
			return v
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomRow(seed *int64, n, high int64) []int64 {
	row := make([]int64, 0, n)
	var v int64
	for int64(len(row)) < n {
		v += 1 + nextRandom(seed)%(2*high/n)
		if cap := high - (n - int64(len(row))) + 1; v > cap {
			v = cap
		}
		row = append(row, v)
	}
	return row
}

func main() {
	highs := []int64{520, 1000, 5000, 10000}
	seed := int64(1198)
	mats := make([][][]int64, 0, 20)
	for k := 0; k < 20; k++ {
		mat := make([][]int64, 0, 500)
		for r := 0; r < 500; r++ {
			mat = append(mat, randomRow(&seed, 500, highs[k%4]))
		}
		mats = append(mats, mat)
	}
	var check int64
	for round := 0; round < 100; round++ {
		for _, mat := range mats {
			v := smallestCommonElement(mat)
			check = (check*131 + v + 2) % 1000000007
		}
	}
	fmt.Printf("100 rounds of 20 matrices of 500 x 500: checksum %d\n", check)
}
