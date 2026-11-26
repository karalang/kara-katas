package main

import "fmt"

func findDiagonalOrder(nums [][]int32) []int32 {
	var diagonals [][]int32
	for i := len(nums) - 1; i >= 0; i-- {
		for j := 0; j < len(nums[i]); j++ {
			for len(diagonals) <= i+j {
				diagonals = append(diagonals, nil)
			}
			diagonals[i+j] = append(diagonals[i+j], nums[i][j])
		}
	}
	var order []int32
	for _, d := range diagonals {
		order = append(order, d...)
	}
	return order
}

func main() {
	var seed int64 = 1424
	pool := make([][]int32, 0, 100000)
	for r := 0; r < 100000; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		n := 1 + seed/65536%9
		var row []int32
		for k := int64(0); k < n; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			row = append(row, int32(1+seed/65536%100000))
		}
		pool = append(pool, row)
	}
	var check int64
	for w := 0; w < 300; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 80001
		for _, x := range findDiagonalOrder(pool[start : start+20000]) {
			check = (check*131 + int64(x)) % 1000000007
		}
	}
	fmt.Printf("300 windows of 2 * 10^4 rows: checksum %d\n", check)
}
