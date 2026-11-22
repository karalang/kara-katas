// LeetCode #2772: Apply Operations to Make All Array Elements Equal to
// Zero -- the bench in Go: the ★ arm over 20 arrays of 10^5 numbers, all
// drawn first, then each answered 40 times.
package main

import "fmt"

func checkArray(nums []int64, k int64) bool {
	n := int64(len(nums))
	ends := make([]int64, n+1)
	var covering int64
	for i := int64(0); i < n; i++ {
		covering -= ends[i]
		left := nums[i] - covering
		if left < 0 {
			return false
		}
		if left > 0 {
			if i+k > n {
				return false
			}
			covering += left
			ends[i+k] += left
		}
	}
	return true
}

var seed int64 = 2772

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func built(n, k, most int64) []int64 {
	nums := make([]int64, n)
	ops := make([]int64, n)
	var running int64
	for i := int64(0); i < n; i++ {
		if i+k <= n {
			ops[i] = nextRandom() % (most + 1)
		}
		running += ops[i]
		if i >= k {
			running -= ops[i-k]
		}
		nums[i] = running
	}
	if nextRandom()%2 == 1 {
		at := wide() % n
		if nums[at] > 0 && nextRandom()%2 == 1 {
			nums[at]--
		} else {
			nums[at]++
		}
	}
	return nums
}

func main() {
	count := 20
	rounds := 40
	cases := make([][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		ks[c] = wide()%1000 + 1
		cases[c] = built(100000, ks[c], 9)
	}
	var yes, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := checkArray(cases[c], ks[c])
			v := int64(1)
			if a {
				yes++
				v = 2
			}
			check = (check*31 + v + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: %d true, checksum %d\n", count, rounds, yes, check)
}
