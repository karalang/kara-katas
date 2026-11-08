// LeetCode #2009: Minimum Number of Operations to Make Array Continuous --
// the ★ arm's benchmark, a mirror of continuous.kara.
package main

import (
	"fmt"
	"sort"
)

func minOperations(nums []int64) int64 {
	n := int64(len(nums))
	values := append([]int64(nil), nums...)
	sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
	m := 0
	for _, v := range values {
		if m == 0 || values[m-1] != v {
			values[m] = v
			m++
		}
	}
	values = values[:m]
	var kept, right int64
	for left := int64(0); left < int64(m); left++ {
		for right < int64(m) && values[right] <= values[left]+n-1 {
			right++
		}
		if right-left > kept {
			kept = right - left
		}
	}
	return n - kept
}

var seed int64 = 2009

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 0, 200)
	for a := int64(0); a < 200; a++ {
		top := 2000 * (a + 1)
		nums := make([]int64, 0, 2000)
		for i := 0; i < 2000; i++ {
			hi := nextRandom()
			nums = append(nums, (hi*32768+nextRandom())%top+1)
		}
		arrays = append(arrays, nums)
	}
	var calls, sum, check int64
	for r := 0; r < 25; r++ {
		for _, nums := range arrays {
			answer := minOperations(nums)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
