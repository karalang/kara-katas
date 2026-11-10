// LeetCode #2091: Removing Minimum and Maximum From Array -- Go mirror of
// the ★ arm's benchmark (deletions.kara): the same 20 shuffled arrays, each
// answered 20 times by the same walk over a slice.
package main

import "fmt"

var seed int64 = 2091

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumDeletions(nums []int64) int64 {
	n := len(nums)
	lo, hi := 0, 0
	for k := 1; k < n; k++ {
		if nums[k] < nums[lo] {
			lo = k
		}
		if nums[k] > nums[hi] {
			hi = k
		}
	}
	i, j := min(lo, hi), max(lo, hi)
	return int64(min(j+1, n-i, i+1+n-j))
}

func main() {
	arrays := make([][]int64, 20)
	for t := range arrays {
		v := make([]int64, 100000)
		for i := range v {
			v[i] = int64(2*i - 100000)
		}
		for i := 99999; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			v[i], v[j] = v[j], v[i]
		}
		arrays[t] = v
	}
	var total, check int64
	for round := 0; round < 20; round++ {
		for t := 0; t < 20; t++ {
			d := minimumDeletions(arrays[(t+round)%20])
			total += d
			check = (check*31 + d) % 1000000007
		}
	}
	fmt.Printf("400 answers: sum %d, checksum %d\n", total, check)
}
