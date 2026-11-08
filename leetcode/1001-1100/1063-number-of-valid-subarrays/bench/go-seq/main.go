// LeetCode #1063: Number of Valid Subarrays -- the benchmark, the same
// left-to-right stack as num_valid.kara.
package main

import "fmt"

func validSubarrays(nums []int64) int64 {
	stack := []int64{}
	var count int64
	for _, x := range nums {
		for len(stack) > 0 && stack[len(stack)-1] > x {
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, x)
		count += int64(len(stack))
	}
	return count
}

var seed int64 = 1063

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// `n` numbers drawn from 0 to `k - 1`.
func randomArray(n, k int64) []int64 {
	a := make([]int64, n)
	for i := range a {
		a[i] = nextRandom() % k
	}
	return a
}

func main() {
	// 20 arrays of 100000 numbers below 2 to 685902, built once, then each
	// answered on 50 of its suffixes
	arrays := [][]int64{}
	for a := int64(0); a < 20; a++ {
		arrays = append(arrays, randomArray(100000, 2+a*a*a*100))
	}
	var calls, total, check int64
	for _, nums := range arrays {
		for p := 0; p < 50; p++ {
			answer := validSubarrays(nums[p*100:])
			total += answer
			check = (check*31 + answer) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: answers sum %d, checksum %d\n", calls, total, check)
}
