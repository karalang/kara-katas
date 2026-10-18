// LeetCode 747 — Largest Number At Least Twice of Others, bench: the ★
// arm (one pass) on millions of 50-value lists cut from a random pool.
// Mirrors dominant_index.kara.
package main

import "fmt"

func dominantIndex(nums []int64) int64 {
	best := 0
	var second int64 = -1
	for i := 1; i < len(nums); i++ {
		if nums[i] > nums[best] {
			second = nums[best]
			best = i
		} else if nums[i] > second {
			second = nums[i]
		}
	}
	if nums[best] >= 2*second {
		return int64(best)
	}
	return -1
}

var seed int64 = 747

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var queries int64 = 2000000
	var poolLen int64 = 100000
	var n int64 = 50
	pool := make([]int64, 0)
	for i := int64(0); i < poolLen; i++ {
		pool = append(pool, nextRandom()%52)
	}
	nums := make([]int64, n)
	var found, total int64
	for q := int64(0); q < queries; q++ {
		start := nextRandom() % (poolLen - n)
		for j := int64(0); j < n; j++ {
			nums[j] = pool[start+j]
		}
		nums[q%n] = 100
		got := dominantIndex(nums)
		if got != -1 {
			found++
			total += got
		}
	}
	fmt.Printf("%d lists of 50 values: %d have a dominant value, indices sum to %d\n", queries, found, total)
}
