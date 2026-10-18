// LeetCode #740: Delete and Earn -- house robber over values.
// Benchmark mirror of the Kara star arm: total the points each value is
// worth in a table as long as the largest value, then walk the values
// in order keeping the best total with the last value taken and with
// it left.
package main

import "fmt"

func deleteAndEarn(nums []int64) int64 {
	var top int64
	for _, x := range nums {
		if x > top {
			top = x
		}
	}
	var points []int64
	for v := int64(0); v < top+1; v++ {
		points = append(points, 0)
	}
	for _, x := range nums {
		points[x] += x
	}
	var take, skip int64
	for v := int64(0); v < top+1; v++ {
		taken := skip + points[v]
		if take > skip {
			skip = take
		}
		take = taken
	}
	if take > skip {
		return take
	}
	return skip
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(740)
	n := int64(20000)
	nums := make([]int64, 0)
	for i := int64(0); i < n; i++ {
		nums = append(nums, 1+nextRandom(&seed)%10000)
	}
	var total int64
	for r := 0; r < 5000; r++ {
		for k := 0; k < 20; k++ {
			j := nextRandom(&seed) % n
			nums[j] = 1 + nextRandom(&seed)%10000
		}
		total += deleteAndEarn(nums)
	}
	fmt.Printf("5000 rounds of 20000 numbers: %d points in all\n", total)
}
