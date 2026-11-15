// LeetCode #2167: Minimum Time to Remove All Cars Containing Illegal Goods
// -- the benchmark's Go mirror of removal.kara.
package main

import (
	"fmt"
	"strings"
)

func minimumTime(s string) int64 {
	n := int64(len(s))
	var left int64
	best := n
	for i, c := range s {
		i := int64(i)
		if c == '1' {
			left = min(left+2, i+1)
		}
		best = min(best, left+n-1-i)
	}
	return best
}

var seed int64 = 2167

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var b strings.Builder
	for i := 0; i < 400000; i++ {
		if nextRandom()%3 == 0 {
			b.WriteByte('1')
		} else {
			b.WriteByte('0')
		}
	}
	train := b.String()
	var check int64
	for r := 0; r < 100; r++ {
		hi := nextRandom()
		start := (hi*32768 + nextRandom()) % 200001
		t := minimumTime(train[start : start+200000])
		check = (check*31 + t) % 1000000007
	}
	fmt.Printf("100 solves: checksum %d\n", check)
}
