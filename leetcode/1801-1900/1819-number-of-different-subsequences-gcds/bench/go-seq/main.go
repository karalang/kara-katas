// LeetCode #1819: Number of Different Subsequences GCDs -- the bench in Go:
// the ★ arm over 100 calls on runs of 50000 to 99999 numbers cut from one
// list of 10^5 numbers from 1 to 2 * 10^5, built once, each run's length
// drawn from the checksum so far.
package main

import (
	"fmt"
	"slices"
)

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func countDifferentSubsequenceGCDs(nums []int64) int64 {
	top := slices.Max(nums)
	present := make([]bool, top+1)
	for _, x := range nums {
		present[x] = true
	}
	var count int64
	for g := int64(1); g <= top; g++ {
		var d int64
		for m := g; m <= top && d != g; m += g {
			if present[m] {
				d = gcd(d, m)
			}
		}
		if d == g {
			count++
		}
	}
	return count
}

var seed int64 = 1819

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom()
		base = append(base, 1+(hi*32768+nextRandom())%200000)
	}
	var check int64
	for call := int64(0); call < 100; call++ {
		n := 50000 + (check+call)%50000
		check = (check*31 + countDifferentSubsequenceGCDs(slices.Clone(base[:n]))) % 1000000007
	}
	fmt.Printf("100 calls: checksum %d\n", check)
}
