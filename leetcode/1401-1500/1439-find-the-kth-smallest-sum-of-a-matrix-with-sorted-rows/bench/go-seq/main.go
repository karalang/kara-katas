package main

import (
	"fmt"
	"slices"
)

func kthSmallest(mat [][]int32, k int32) int32 {
	sums := []int32{0}
	for _, row := range mat {
		next := make([]int32, 0, len(sums)*len(row))
		for _, s := range sums {
			for _, x := range row {
				next = append(next, s+x)
			}
		}
		slices.Sort(next)
		if len(next) > int(k) {
			next = next[:k]
		}
		sums = next
	}
	return sums[k-1]
}

func main() {
	var seed int64 = 1439
	var check int64
	for c := 0; c < 300; c++ {
		mat := make([][]int32, 0, 40)
		for r := 0; r < 40; r++ {
			row := make([]int32, 0, 40)
			for j := 0; j < 40; j++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				row = append(row, int32(1+seed/65536%5000))
			}
			slices.Sort(row)
			mat = append(mat, row)
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		k := int32(1 + seed/65536%200)
		check = (check*131 + int64(kthSmallest(mat, k))) % 1000000007
	}
	fmt.Printf("300 matrices of 40 by 40: checksum %d\n", check)
}
