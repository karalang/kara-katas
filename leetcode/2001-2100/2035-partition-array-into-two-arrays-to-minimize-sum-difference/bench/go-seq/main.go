// LeetCode #2035: Partition Array Into Two Arrays to Minimize Sum
// Difference -- the ★ arm in Go, the same algorithm and workload as
// partition.kara: each half's subset sums listed by size, the right lists
// sorted, and sort.Search for the right sum that brings the side to half
// the total, with the sums on either side tried.
package main

import (
	"fmt"
	"math"
	"sort"
)

func subsetSums(half []int64) [][]int64 {
	n := len(half)
	bySize := make([][]int64, n+1)
	for mask := 0; mask < 1<<n; mask++ {
		var sum int64
		size := 0
		for i := 0; i < n; i++ {
			if mask>>i&1 == 1 {
				sum += half[i]
				size++
			}
		}
		bySize[size] = append(bySize[size], sum)
	}
	return bySize
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func minimumDifference(nums []int64) int64 {
	n := len(nums) / 2
	var total int64
	for _, v := range nums {
		total += v
	}
	left := subsetSums(nums[0:n])
	right := subsetSums(nums[n : 2*n])
	for _, list := range right {
		sort.Slice(list, func(i, j int) bool { return list[i] < list[j] })
	}
	best := int64(math.MaxInt64)
	for k := 0; k <= n; k++ {
		others := right[n-k]
		for _, a := range left[k] {
			at := sort.Search(len(others), func(i int) bool { return 2*(a+others[i]) >= total })
			if at < len(others) {
				if d := abs(total - 2*(a+others[at])); d < best {
					best = d
				}
			}
			if at > 0 {
				if d := abs(total - 2*(a+others[at-1])); d < best {
					best = d
				}
			}
		}
	}
	return best
}

var seed int64 = 2035

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	tops := []int64{10000000, 1000, 100, 10000000, 50}
	arrays := make([][]int64, 40)
	for a := 0; a < 40; a++ {
		top := tops[a%5]
		nums := make([]int64, 30)
		for i := range nums {
			hi := nextRandom()
			lo := nextRandom()
			nums[i] = (hi*32768+lo)%(2*top+1) - top
		}
		arrays[a] = nums
	}
	var calls, sum, check int64
	for round := 0; round < 5; round++ {
		for a := 0; a < 40; a++ {
			at := (round*7 + a*3) % 30
			arrays[a][at] = -arrays[a][at]
			answer := minimumDifference(arrays[a])
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
