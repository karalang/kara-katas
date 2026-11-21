// LeetCode #2441: Largest Positive Integer That Exists With Its Negative
// -- the bench, the ★ arm: a table of 2001 flags, offset by 1000, and
// the largest magnitude whose negative was seen.
package main

import "fmt"

func findMaxK(nums []int64) int64 {
	seen := make([]bool, 2001)
	best := int64(-1)
	for _, x := range nums {
		if seen[1000-x] {
			a := x
			if a < 0 {
				a = -a
			}
			if a > best {
				best = a
			}
		}
		seen[1000+x] = true
	}
	return best
}

var seed int64 = 2441

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func nonzero() int64 {
	v := 1 + nextRandom()%1000
	if nextRandom()%2 == 0 {
		return v
	}
	return -v
}

func main() {
	arrays := make([][]int64, 100)
	for c := range arrays {
		arrays[c] = make([]int64, 1000)
		for i := range arrays[c] {
			arrays[c][i] = nonzero()
		}
	}
	var check int64
	for p := int64(0); p < 1000; p++ {
		for c := range arrays {
			at := (p*7919 + int64(c)*104729) % 1000
			arrays[c][at] = nonzero()
			check = (check*31 + findMaxK(arrays[c]) + p) % 1000000007
		}
	}
	fmt.Printf("1000 passes over 100 arrays of 1000 values: checksum %d\n", check)
}
