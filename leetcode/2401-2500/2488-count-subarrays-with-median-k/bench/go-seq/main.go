// LeetCode #2488: Count Subarrays With Median K -- Go mirror of the ★ arm's
// benchmark (median.kara): the same 20 orders and passes, the balances of
// the starts counted in a `map[int64]int64`.
package main

import "fmt"

func countSubarrays(nums []int64, k int64) int64 {
	n := len(nums)
	at := 0
	for nums[at] != k {
		at++
	}
	starts := map[int64]int64{0: 1}
	balance := int64(0)
	for i := at - 1; i >= 0; i-- {
		if nums[i] > k {
			balance++
		} else {
			balance--
		}
		starts[balance]++
	}
	count := int64(0)
	balance = 0
	for j := at; j < n; j++ {
		if j > at {
			if nums[j] > k {
				balance++
			} else {
				balance--
			}
		}
		count += starts[-balance] + starts[1-balance]
	}
	return count
}

var seed int64 = 2488

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(10000)
	passes := int64(400)
	orders := make([][]int64, 20)
	for o := range orders {
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = int64(i) + 1
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom() % (i + 1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		orders[o] = nums
	}
	check := int64(0)
	for p := int64(0); p < passes; p++ {
		for o := int64(0); o < 20; o++ {
			nums := orders[o]
			a, b := check%n, (check/n+p)%n
			nums[a], nums[b] = nums[b], nums[a]
			k := (check+o)%n + 1
			check = (check*31 + countSubarrays(nums, k) + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 20 orders of 10^4: checksum %d\n", passes, check)
}
