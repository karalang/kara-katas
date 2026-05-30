// Benchmark workload — 4Sum (LeetCode #18).
// Go mirror of ../four_sum.kara. Same M/N/K, LCG generator, per-case target
// bag, sort + two-fix + two-pointer body with dedup and min/max prunes, and
// sink — see that file's header for the rationale.

package main

import (
	"fmt"
	"sort"
)

func fourSum(nums []int64, target int64) [][]int64 {
	s := make([]int64, len(nums))
	copy(s, nums)
	sort.Slice(s, func(a, b int) bool { return s[a] < s[b] })
	n := int64(len(s))
	result := [][]int64{}
	var a int64 = 0
	for a < n-3 {
		if a > 0 && s[a] == s[a-1] {
			a++
			continue
		}
		if s[a]+s[a+1]+s[a+2]+s[a+3] > target {
			break
		}
		if s[a]+s[n-1]+s[n-2]+s[n-3] < target {
			a++
			continue
		}
		b := a + 1
		for b < n-2 {
			if b > a+1 && s[b] == s[b-1] {
				b++
				continue
			}
			if s[a]+s[b]+s[b+1]+s[b+2] > target {
				break
			}
			if s[a]+s[b]+s[n-1]+s[n-2] < target {
				b++
				continue
			}
			lo, hi := b+1, n-1
			for lo < hi {
				sum := s[a] + s[b] + s[lo] + s[hi]
				if sum < target {
					lo++
				} else if sum > target {
					hi--
				} else {
					result = append(result, []int64{s[a], s[b], s[lo], s[hi]})
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
			b++
		}
		a++
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

var targetBag = [8]int64{-20, -8, -3, 0, 2, 6, 12, 24}

func targetFor(idx int64) int64 {
	return targetBag[idx]
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
		r := fourSum(sets[idx], targetFor(idx))
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
