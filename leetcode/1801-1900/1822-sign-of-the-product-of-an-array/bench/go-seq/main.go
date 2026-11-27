// LeetCode #1822: Sign of the Product of an Array -- the bench in Go: the ★
// arm over 300000 calls on runs of 500 to 999 numbers cut from one list of
// 2000 numbers from -100 to 100 but zero, built once, each run's start and
// length drawn from the checksum so far.
package main

import (
	"fmt"
	"slices"
)

func arraySign(nums []int64) int64 {
	var sign int64 = 1
	for _, x := range nums {
		if x == 0 {
			return 0
		}
		if x < 0 {
			sign = -sign
		}
	}
	return sign
}

var seed int64 = 1822

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	base := make([]int64, 0, 2000)
	for i := 0; i < 2000; i++ {
		x := nextRandom()%200 - 100
		if x >= 0 {
			x++
		}
		base = append(base, x)
	}
	var check int64
	for call := int64(0); call < 300000; call++ {
		start := (check + call) % 1000
		n := 500 + (check*7+call)%500
		check = (check*3 + arraySign(slices.Clone(base[start:start+n])) + 1) % 1000000007
	}
	fmt.Printf("300000 calls: checksum %d\n", check)
}
