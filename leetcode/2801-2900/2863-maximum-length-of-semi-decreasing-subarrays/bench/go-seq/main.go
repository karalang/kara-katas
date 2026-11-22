// LeetCode #2863: Maximum Length of Semi-Decreasing Subarrays -- the
// bench: the ★ arm over 100 arrays of 10^5 values, LeetCode's most,
// every other one random over LeetCode's range and the rest rising with
// five values moved, all drawn first, then each answered 10 times.
package main

import "fmt"

func maxSubarrayLength(nums []int64) int64 {
	n := len(nums)
	starts := make([]int, 0)
	for i := 0; i < n; i++ {
		if len(starts) == 0 || nums[i] > nums[starts[len(starts)-1]] {
			starts = append(starts, i)
		}
	}
	var best int64
	for j := n - 1; j >= 0; j-- {
		for len(starts) > 0 {
			i := starts[len(starts)-1]
			if nums[i] <= nums[j] {
				break
			}
			best = max(best, int64(j-i+1))
			starts = starts[:len(starts)-1]
		}
	}
	return best
}

var seed int64 = 2863

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 100, 10, 100000
	arrays := make([][]int64, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, n)
		for i := range nums {
			if c%2 == 0 {
				nums[i] = wide()%2000000001 - 1000000000
			} else {
				nums[i] = 20000*int64(i) - 1000000000
			}
		}
		if c%2 == 1 {
			for k := 0; k < 5; k++ {
				i := wide() % n
				nums[i] = wide()%2000000001 - 1000000000
			}
		}
		arrays[c] = nums
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			longest := maxSubarrayLength(nums)
			total += longest
			check = (check*31 + longest + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: lengths total %d, checksum %d\n", count, n, rounds, total, check)
}
