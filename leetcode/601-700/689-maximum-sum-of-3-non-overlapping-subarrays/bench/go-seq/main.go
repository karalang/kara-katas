// LeetCode #689: Maximum Sum of 3 Non-Overlapping Subarrays -- best to
// each side. Bench.
//
// 100 arrays of 20,000 values from 1 to 65535, each with a k from 1 to
// 1,000, are built once; then 20 rounds answer every array.

package main

import "fmt"

func maxSumOfThreeSubarrays(nums []int64, k int64) []int64 {
	n := int64(len(nums))
	count := n - k + 1
	w := make([]int64, count)
	var sum int64
	for i := int64(0); i < n; i++ {
		sum += nums[i]
		if i >= k {
			sum -= nums[i-k]
		}
		if i >= k-1 {
			w[i-k+1] = sum
		}
	}
	left := make([]int64, count)
	var best int64
	for i := int64(0); i < count; i++ {
		if w[i] > w[best] {
			best = i
		}
		left[i] = best
	}
	right := make([]int64, count)
	best = count - 1
	for i := count - 1; i >= 0; i-- {
		if w[i] >= w[best] {
			best = i
		}
		right[i] = best
	}
	var answer []int64
	var top int64 = -1
	for j := k; j < count-k; j++ {
		a := left[j-k]
		c := right[j+k]
		total := w[a] + w[j] + w[c]
		if total > top {
			top = total
			answer = []int64{a, j, c}
		}
	}
	return answer
}

var seed int64 = 689

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 100, 20
	arrays := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, 20000)
		for i := 0; i < 20000; i++ {
			nums = append(nums, 1+nextRandom()%65535)
		}
		arrays[c] = nums
		ks[c] = 1 + nextRandom()%1000
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			got := maxSumOfThreeSubarrays(arrays[c], ks[c])
			sum = (sum*31 + got[0] + got[1] + got[2] + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays answered, checksum %d\n", count*rounds, sum)
}
