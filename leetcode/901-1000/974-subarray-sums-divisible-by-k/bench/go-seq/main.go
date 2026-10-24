// Benchmark: LeetCode #974 Subarray Sums Divisible by K -- the ★ arm,
// counts of prefix remainders, on 20 arrays of 30000 random numbers.
// Mirrors subarrays_div_by_k.kara, .rs, .c and .py.
package main

import "fmt"

func subarraysDivByK(nums []int64, k int64) int64 {
	count := make([]int64, k)
	count[0] = 1
	var sum, total int64
	for _, x := range nums {
		sum += x
		r := (sum%k + k) % k
		total += count[r]
		count[r]++
	}
	return total
}

var seed int64 = 974

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count := 200, 20
	type kase struct {
		nums []int64
		k    int64
	}
	cases := make([]kase, count)
	for c := range cases {
		nums := make([]int64, 30000)
		for i := range nums {
			nums[i] = nextRandom()%20001 - 10000
		}
		cases[c] = kase{nums, 2 + nextRandom()%9999}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			c := cases[(r+i)%count]
			got := subarraysDivByK(c.nums, c.k)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of 30000 numbers: %d subarrays, checksum %d\n", rounds, count, total, check)
}
