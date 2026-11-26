// LeetCode #1477: Find Two Non-overlapping Sub-arrays Each With Target
// Sum -- bench, Go mirror of min_sum_of_lengths.kara
package main

import "fmt"

func minSumOfLengths(arr []int32, target int32) int32 {
	n := int64(len(arr))
	none := n + 1
	shortest := make([]int64, n)
	best := 2 * none
	var sum int64
	var left int64
	for right := int64(0); right < n; right++ {
		sum += int64(arr[right])
		for sum > int64(target) {
			sum -= int64(arr[left])
			left++
		}
		here := none
		if sum == int64(target) {
			here = right - left + 1
			if left > 0 && shortest[left-1] < none {
				best = min(best, here+shortest[left-1])
			}
		}
		if right > 0 {
			shortest[right] = min(shortest[right-1], here)
		} else {
			shortest[right] = here
		}
	}
	if best >= 2*none {
		return -1
	}
	return int32(best)
}

var seed int64 = 1477

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arr := make([]int32, 100000)
	for i := range arr {
		arr[i] = int32(1 + nextRandom()%1000)
	}
	var check int64
	for pass := int64(0); pass < 400; pass++ {
		arr[check%100000] = int32(1 + (check/7)%1000)
		target := int32(500 + check%20000)
		got := minSumOfLengths(arr, target)
		check = (check*31 + int64(got) + 1 + pass) % 1000000007
	}
	fmt.Printf("400 passes over 100000 values: checksum %d\n", check)
}
