// LeetCode #2148: Count Elements With Strictly Smaller and Greater
// Elements -- the benchmark's Go mirror of elements.kara.
package main

import "fmt"

func countElements(nums []int64) int64 {
	low, high := nums[0], nums[0]
	for _, x := range nums {
		if x < low {
			low = x
		}
		if x > high {
			high = x
		}
	}
	var count int64
	for _, x := range nums {
		if low < x && x < high {
			count++
		}
	}
	return count
}

var seed int64 = 2148

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	pool := make([]int64, 100000)
	for i := range pool {
		pool[i] = nextRandom()*7%200001 - 100000
	}
	var total, check int64
	for round := int64(0); round < 200000; round++ {
		at := nextRandom() % 100000
		pool[at] = nextRandom()%21 - 10
		from := nextRandom() % (100000 - 100)
		nums := make([]int64, 100)
		copy(nums, pool[from:from+100])
		count := countElements(nums)
		total += count
		check = (check*31 + count + round) % 1000000007
	}
	fmt.Printf("200000 counts: %d counted in all, checksum %d\n", total, check)
}
