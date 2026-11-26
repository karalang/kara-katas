package main

import "fmt"

func minStartValue(nums []int32) int32 {
	var sum, lowest int32
	for _, x := range nums {
		sum += x
		if sum < lowest {
			lowest = sum
		}
	}
	return 1 - lowest
}

func main() {
	var seed int64 = 1413
	pool := make([]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		pool = append(pool, int32(seed/65536%201-100))
	}
	var check int64
	for i := 0; i < 3000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 99901
		check = (check*131 + int64(minStartValue(pool[start:start+100]))) % 1000000007
	}
	fmt.Printf("3 * 10^6 windows of 100 numbers: checksum %d\n", check)
}
