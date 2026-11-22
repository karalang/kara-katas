// LeetCode #2875: Minimum Size Subarray in Infinite Array -- the bench,
// as infinite.kara: 50 arrays of 10^5 values, each with its target,
// answered 20 times by the sliding-window arm.
package main

import "fmt"

func minSizeSubarray(nums []int64, target int64) int64 {
	n := int64(len(nums))
	var total int64
	for _, v := range nums {
		total += v
	}
	whole, rest := target/total*n, target%total
	if rest == 0 {
		return whole
	}
	var best, sum, left int64 = -1, 0, 0
	for right := int64(0); right < 2*n; right++ {
		sum += nums[right%n]
		for sum > rest {
			sum -= nums[left%n]
			left++
		}
		if sum == rest && (best < 0 || right-left+1 < best) {
			best = right - left + 1
		}
	}
	if best < 0 {
		return -1
	}
	return whole + best
}

var seed int64 = 2875

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 50, 20, 100000
	arrays := make([][]int64, count)
	targets := make([]int64, count)
	for c := range arrays {
		top := int64(100000)
		if c%2 == 1 {
			top = 10
		}
		nums := make([]int64, n)
		for i := range nums {
			nums[i] = wide()%top + 1
		}
		arrays[c] = nums
		targets[c] = wide()%1000000000 + 1
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c, nums := range arrays {
			length := minSizeSubarray(nums, targets[c])
			total += length
			check = (check*31 + length + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: lengths total %d, checksum %d\n", count, n, rounds, total, check)
}
