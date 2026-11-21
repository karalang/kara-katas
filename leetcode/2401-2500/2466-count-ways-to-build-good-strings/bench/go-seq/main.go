// LeetCode #2466: Count Ways To Build Good Strings -- the bench, the ★ arm
// in Go: bottom-up counts in a slice, each length's the sum of the counts
// one block back, and the counts from `low` to `high` summed.
package main

import "fmt"

const MOD = 1000000007

func countGoodStrings(low, high, zero, one int64) int64 {
	ways := make([]int64, high+1)
	ways[0] = 1
	var total int64
	for l := int64(1); l <= high; l++ {
		if l >= zero {
			ways[l] = (ways[l] + ways[l-zero]) % MOD
		}
		if l >= one {
			ways[l] = (ways[l] + ways[l-one]) % MOD
		}
		if l >= low {
			total = (total + ways[l]) % MOD
		}
	}
	return total
}

var seed int64 = 2466

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 cases built once, `high` from 50000 to 10^5, `low` from 1 to
	// `high`, blocks of 1 to 20 no longer than `low`; then 28 passes,
	// each setting every case's zero block from the checksum so far, then
	// answering it and folding the answer plus the pass into the checksum
	type kase struct{ low, high, zero, one int64 }
	cases := []kase{}
	for i := 0; i < 20; i++ {
		r1 := nextRandom()
		high := 50000 + (r1*32768+nextRandom())%50001
		r3 := nextRandom()
		low := 1 + (r3*32768+nextRandom())%high
		zero := 1 + nextRandom()%min(low, 20)
		one := 1 + nextRandom()%min(low, 20)
		cases = append(cases, kase{low, high, zero, one})
	}
	var check int64
	for p := int64(0); p < 28; p++ {
		for a := range cases {
			c := &cases[a]
			c.zero = 1 + (check+int64(a))%min(c.low, 20)
			check = (check*31 + countGoodStrings(c.low, c.high, c.zero, c.one) + p) % 1000000007
		}
	}
	fmt.Printf("28 passes over 20 cases up to 10^5: checksum %d\n", check)
}
