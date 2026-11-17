// LeetCode #2239: Find Closest Number to Zero -- the benchmark's Go
// mirror of closest.kara: one scan, a number kept when nearer to zero,
// or as near and larger.
package main

import "fmt"

func magnitude(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func findClosestNumber(nums []int64) int64 {
	closest := nums[0]
	for _, x := range nums {
		if magnitude(x) < magnitude(closest) || (magnitude(x) == magnitude(closest) && x > closest) {
			closest = x
		}
	}
	return closest
}

var seed int64 = 2239

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	nums := make([]int64, 1000)
	for i := range nums {
		nums[i] = wideRandom()%200001 - 100000
	}
	check := int64(0)
	for pass := 0; pass < 100000; pass++ {
		// punch: one number drawn again before each pass
		at := nextRandom() % 1000
		nums[at] = wideRandom()%200001 - 100000
		check = (check*31 + findClosestNumber(nums) + 100000) % 1000000007
	}
	fmt.Printf("100000 passes over 1000 numbers: checksum %d\n", check)
}
