// LeetCode #1033: Moving Stones Until Consecutive -- bench
// Mirrors ../moving_stones.kara; see ../../README.md § Benchmarks.
package main

import (
	"fmt"
	"sort"
)

func numMovesStones(a, b, c int64) []int64 {
	s := []int64{a, b, c}
	sort.Slice(s, func(i, j int) bool { return s[i] < s[j] })
	x, y, z := s[0], s[1], s[2]
	var fewest int64
	if z-x == 2 {
		fewest = 0
	} else if y-x <= 2 || z-y <= 2 {
		fewest = 1
	} else {
		fewest = 2
	}
	return []int64{fewest, z - x - 2}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000000
	rounds := 40
	seed := int64(1033)
	cases := make([][3]int64, 0, count)
	for len(cases) < count {
		a := nextRandom(&seed)%100 + 1
		b := nextRandom(&seed)%100 + 1
		c := nextRandom(&seed)%100 + 1
		if a != b && b != c && a != c {
			cases = append(cases, [3]int64{a, b, c})
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, t := range cases {
			moves := numMovesStones(t[0], t[1], t[2])
			total += moves[0] + moves[1]
			check = (check*131 + moves[0]*101 + moves[1]) % 1000000007
		}
	}
	fmt.Printf("%d triples, %d rounds: sum %d, checksum %d\n", count, rounds, total, check)
}
