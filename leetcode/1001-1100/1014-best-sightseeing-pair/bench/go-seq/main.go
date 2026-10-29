// LeetCode #1014: Best Sightseeing Pair -- bench
// Mirrors ../sightseeing.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

func maxScoreSightseeingPair(values []int64) int64 {
	bestFirst := values[0]
	var best int64
	for j := 1; j < len(values); j++ {
		if score := bestFirst + values[j] - int64(j); score > best {
			best = score
		}
		if v := values[j] + int64(j); v > bestFirst {
			bestFirst = v
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := int64(50000)
	rounds := 10000
	seed := int64(1014)
	values := make([]int64, 0, count)
	for i := int64(0); i < count; i++ {
		values = append(values, 1+nextRandom(&seed)%1000)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		at := (hi*32768 + lo) % count
		values[at] = 1 + nextRandom(&seed)%1000
		answer := maxScoreSightseeingPair(values)
		total += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds over %d values: answers sum to %d, checksum %d\n", rounds, count, total, check)
}
