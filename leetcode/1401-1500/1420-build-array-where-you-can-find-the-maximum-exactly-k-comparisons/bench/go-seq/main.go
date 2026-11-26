package main

import "fmt"

func numOfArrays(n, m, k int32) int32 {
	const modulus int64 = 1000000007
	table := func() [][]int64 {
		t := make([][]int64, m+1)
		for j := range t {
			t[j] = make([]int64, k+1)
		}
		return t
	}
	ways := table()
	if k >= 1 {
		for j := int32(1); j <= m; j++ {
			ways[j][1] = 1
		}
	}
	for i := int32(1); i < n; i++ {
		next := table()
		for c := int32(1); c <= k; c++ {
			var below int64
			for j := int32(1); j <= m; j++ {
				next[j][c] = (ways[j][c]*int64(j) + below) % modulus
				below = (below + ways[j][c-1]) % modulus
			}
		}
		ways = next
	}
	var total int64
	for j := int32(1); j <= m; j++ {
		total = (total + ways[j][k]) % modulus
	}
	return int32(total)
}

func main() {
	var seed, check int64 = 1420, 0
	for i := 0; i < 1000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		k := seed / 65536 % 51
		check = (check*131 + int64(numOfArrays(50, 100, int32(k)))) % 1000000007
	}
	fmt.Printf("1000 values of k at n = 50, m = 100: checksum %d\n", check)
}
