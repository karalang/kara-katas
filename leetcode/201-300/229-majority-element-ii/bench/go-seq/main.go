package main

import "fmt"

func windowMajoritySum(nums []int64, s int64, win int64) int64 {
	var cand1, cand2, count1, count2 int64
	end := s + win
	for k := s; k < end; k++ {
		x := nums[k]
		if count1 > 0 && x == cand1 {
			count1 += 1
		} else if count2 > 0 && x == cand2 {
			count2 += 1
		} else if count1 == 0 {
			cand1 = x
			count1 = 1
		} else if count2 == 0 {
			cand2 = x
			count2 = 1
		} else {
			count1 -= 1
			count2 -= 1
		}
	}

	var real1, real2 int64
	for j := s; j < end; j++ {
		x := nums[j]
		if count1 > 0 && x == cand1 {
			real1 += 1
		} else if count2 > 0 && x == cand2 {
			real2 += 1
		}
	}

	threshold := win / 3
	var total int64 = 0
	if count1 > 0 && real1 > threshold {
		total += cand1
	}
	if count2 > 0 && real2 > threshold {
		total += cand2
	}
	return total
}

func main() {
	var n int64 = 3000000
	var win int64 = 16

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums = append(nums, (state%3)+1)
	}

	var sink int64 = 0
	last := n - win
	for s := int64(0); s <= last; s++ {
		sink += windowMajoritySum(nums, s, win)
	}
	fmt.Println(sink)
}
