// LeetCode #2016: Maximum Difference Between Increasing Elements -- the ★
// arm's benchmark, a mirror of difference.kara.
package main

import "fmt"

func maximumDifference(nums []int64) int64 {
	smallest, best := nums[0], int64(-1)
	for _, x := range nums[1:] {
		if x > smallest && x-smallest > best {
			best = x - smallest
		}
		if x < smallest {
			smallest = x
		}
	}
	return best
}

var seed int64 = 2016

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 1000)
	for a := int64(0); a < 1000; a++ {
		fall := a % 11
		nums := make([]int64, 0, 10000)
		for i := 0; i < 10000; i++ {
			if i > 0 && nextRandom()%10 < fall {
				v := nums[i-1] - nextRandom()%1000
				if v < 1 {
					v = 1
				}
				nums = append(nums, v)
			} else {
				hi := nextRandom()
				nums = append(nums, (hi*32768+nextRandom())%1000000000+1)
			}
		}
		arrays = append(arrays, nums)
	}
	var calls, sum, check int64
	for r := 0; r < 10; r++ {
		for _, nums := range arrays {
			answer := maximumDifference(nums)
			calls++
			sum += answer
			check = (check*31 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
