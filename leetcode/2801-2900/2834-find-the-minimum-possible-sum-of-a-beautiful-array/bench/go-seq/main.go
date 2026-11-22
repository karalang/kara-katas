// LeetCode #2834: Find the Minimum Possible Sum of a Beautiful Array --
// the bench, mirrored from sum.kara: two arithmetic series.
package main

import "fmt"

const mod = 1000000007

func minimumPossibleSum(n, target int64) int64 {
	low := n
	if target/2 < low {
		low = target / 2
	}
	high := n - low
	first := low * (low + 1) / 2
	rest := high * (2*target + high - 1) / 2
	return (first + rest) % mod
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	const count, rounds = 1000000, 20
	seed := int64(2834)
	ns := make([]int64, count)
	ts := make([]int64, count)
	for i := 0; i < count; i++ {
		ns[i] = wide(&seed)%1000000000 + 1
		ts[i] = wide(&seed)%1000000000 + 1
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for i := 0; i < count; i++ {
			check = (check*31 + minimumPossibleSum(ns[i], ts[i]) + r) % mod
		}
	}
	fmt.Printf("%d pairs, %d rounds: checksum %d\n", count, rounds, check)
}
