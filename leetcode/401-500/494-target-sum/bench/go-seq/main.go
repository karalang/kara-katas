// Benchmark for #494: Go mirror of the ★ arm (counting ways by running
// sum); see ../target_sum.kara.
package main

import "fmt"

func findTargetSumWays(nums []int64, target int64) int64 {
	var total int64
	for _, x := range nums {
		total += x
	}
	if target > total || target < -total {
		return 0
	}
	width := 2*total + 1
	ways := make([]int64, width)
	ways[total] = 1
	for _, x := range nums {
		next := make([]int64, width)
		for s := int64(0); s < width; s++ {
			if ways[s] > 0 {
				next[s+x] += ways[s]
				next[s-x] += ways[s]
			}
		}
		ways = next
	}
	return ways[target+total]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 40,000 arrays of 20 numbers from 0 to 50 (the problem's most numbers
	// and at most its largest sum), each with a target from -100 to 100,
	// built once, then each solved once.
	var arrays [][]int64
	var targets []int64
	var seed int64 = 494
	for k := 0; k < 40000; k++ {
		nums := make([]int64, 0, 20)
		for i := 0; i < 20; i++ {
			nums = append(nums, nextRandom(&seed)%51)
		}
		arrays = append(arrays, nums)
		targets = append(targets, nextRandom(&seed)%201-100)
	}
	reachable := 0
	var checksum int64
	for k := range arrays {
		ways := findTargetSumWays(arrays[k], targets[k])
		if ways > 0 {
			reachable++
		}
		checksum = (checksum*31 + ways) % 1000000007
	}
	fmt.Printf("40000 arrays of 20: %d reachable, checksum %d\n", reachable, checksum)
}
