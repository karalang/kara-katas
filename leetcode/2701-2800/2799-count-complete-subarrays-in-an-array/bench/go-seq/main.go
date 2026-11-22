// LeetCode #2799: Count Complete Subarrays in an Array -- the bench in
// Go: the ★ arm over 2000 arrays of 1000 numbers, half from 1 to 2000
// and half from 1 to 20, all drawn first, then each answered 20 times.
package main

import "fmt"

func countCompleteSubarrays(nums []int64) int64 {
	distinct := map[int64]bool{}
	for _, v := range nums {
		distinct[v] = true
	}
	d := len(distinct)
	counts := map[int64]int64{}
	start := 0
	var complete int64
	for _, v := range nums {
		counts[v]++
		for len(counts) == d {
			first := nums[start]
			held := counts[first]
			if held == 1 {
				break
			}
			counts[first] = held - 1
			start++
		}
		if len(counts) == d {
			complete += int64(start) + 1
		}
	}
	return complete
}

var seed int64 = 2799

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 2000
	rounds := 20
	cases := make([][]int64, count)
	for c := 0; c < count; c++ {
		var top int64 = 2000
		if c%2 == 1 {
			top = 20
		}
		cases[c] = make([]int64, 1000)
		for i := range cases[c] {
			cases[c][i] = wide()%top + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := countCompleteSubarrays(cases[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 1000, %d rounds: complete sum to %d, checksum %d\n", count, rounds, total, check)
}
