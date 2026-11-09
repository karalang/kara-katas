// LeetCode #2036: Maximum Alternating Subarray Sum -- the ★ arm in Go, the
// same algorithm and workload as alternating.kara: the best sum ending here
// on a plus, and the one ending on a minus (none yet at the first value, a
// flag for the Option), stepped once per value.
package main

import "fmt"

func maximumAlternatingSubarraySum(nums []int64) int64 {
	plus := nums[0]
	var minus int64
	hasMinus := false
	best := plus
	for _, x := range nums[1:] {
		nextPlus := x
		if hasMinus {
			nextPlus = max(x, minus+x)
		}
		minus = plus - x
		hasMinus = true
		plus = nextPlus
		best = max(best, plus)
		best = max(best, minus)
	}
	return best
}

var seed int64 = 2036

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	tops := []int64{100000, 1000, 100000, 3}
	arrays := make([][]int64, 4)
	for a := 0; a < 4; a++ {
		nums := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			hi := nextRandom()
			lo := nextRandom()
			nums = append(nums, (hi*32768+lo)%(2*tops[a]+1)-tops[a])
		}
		arrays[a] = nums
	}
	var calls, sum, check int64
	for round := int64(0); round < 1000; round++ {
		for a := int64(0); a < 4; a++ {
			at := (round*7919 + a*104729) % 100000
			arrays[a][at] = -arrays[a][at]
			answer := maximumAlternatingSubarraySum(arrays[a])
			calls++
			sum += answer
			check = (check*31 + answer%1000000007) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
