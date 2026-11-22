// LeetCode #2789: Largest Element in an Array after Merge Operations --
// the bench in Go: the ★ arm over 20 arrays of 10^5 numbers up to 10^6,
// all drawn first, then each answered 100 times.
package main

import "fmt"

func maxArrayValue(nums []int64) int64 {
	n := len(nums)
	held := nums[n-1]
	for i := n - 2; i >= 0; i-- {
		if nums[i] <= held {
			held += nums[i]
		} else {
			held = nums[i]
		}
	}
	return held
}

var seed int64 = 2789

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 100
	cases := make([][]int64, count)
	for c := 0; c < count; c++ {
		cases[c] = make([]int64, 100000)
		for i := range cases[c] {
			cases[c][i] = wide()%1000000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := maxArrayValue(cases[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: largest sum to %d, checksum %d\n", count, rounds, total, check)
}
