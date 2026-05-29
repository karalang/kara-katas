// Benchmark workload — 3Sum (LeetCode #15).
// Go mirror of bench/three_sum.kara. Same M/N/K, LCG generator, sort +
// two-pointer dedup, and sink — see that file's header for the rationale.

package main

import (
	"fmt"
	"sort"
)

func threeSum(nums []int64) [][]int64 {
	s := make([]int64, len(nums))
	copy(s, nums)
	sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
	n := int64(len(s))
	result := [][]int64{}
	var i int64 = 0
	for i < n-2 {
		if i > 0 && s[i] == s[i-1] {
			i++
			continue
		}
		if s[i] > 0 {
			break
		}
		lo, hi := i+1, n-1
		for lo < hi {
			sum := s[i] + s[lo] + s[hi]
			if sum < 0 {
				lo++
			} else if sum > 0 {
				hi--
			} else {
				result = append(result, []int64{s[i], s[lo], s[hi]})
				lo++
				hi--
				for lo < hi && s[lo] == s[lo-1] {
					lo++
				}
				for lo < hi && s[hi] == s[hi+1] {
					hi--
				}
			}
		}
		i++
	}
	return result
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
func lcgNext(state int64) int64 {
	return (1103515245*state + 12345) % 2147483648
}

func buildCase(seed, count int64) []int64 {
	v := make([]int64, 0, count)
	state := seed
	for j := int64(0); j < count; j++ {
		state = lcgNext(state)
		v = append(v, (state%21)-10)
	}
	return v
}

func main() {
	const mCases int64 = 8
	const nValues int64 = 16
	const kIters int64 = 1000000

	sets := make([][]int64, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(m*1000003+12345, nValues)
	}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % mCases
		r := threeSum(sets[idx])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
