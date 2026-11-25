// LeetCode #1394 bench, Go mirror of the ★ arm.
package main

import "fmt"

func findLucky(arr []int32) int32 {
	count := make([]int32, 501)
	for _, x := range arr {
		count[x]++
	}
	for x := int32(500); x >= 1; x-- {
		if count[x] == x {
			return x
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n = 500
	var seed int64 = 1394
	arr := make([]int32, n)
	for k := range arr {
		arr[k] = int32(1 + nextRandom(&seed)%40)
	}
	var check int64
	for round := 0; round < 600000; round++ {
		seed = (seed + check) % 2147483648
		i := nextRandom(&seed) % n
		arr[i] = int32(1 + nextRandom(&seed)%40)
		check = (check*131 + int64(findLucky(arr)) + 1) % 1000000007
	}
	fmt.Printf("600000 rounds over 500 values: checksum %d\n", check)
}
