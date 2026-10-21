// Benchmark for #830: Positions of Large Groups -- the ★ arm (two pointers).
//
// Mirrors large_group_positions.kara: from the start i of each group, j
// runs on while the letter stays the same, and the group s[i..j] is kept
// when it holds 3 or more.
package main

import (
	"fmt"
	"strings"
)

func largeGroupPositions(s string) [][]int64 {
	n := int64(len(s))
	var groups [][]int64
	i := int64(0)
	for i < n {
		j := i
		for j < n && s[j] == s[i] {
			j++
		}
		if j-i >= 3 {
			groups = append(groups, []int64{i, j - 1})
		}
		i = j
	}
	return groups
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = int64(64), int64(200000), 1000
	seed := int64(830)
	strs := make([]string, 0, count)
	for g := int64(0); g < count; g++ {
		letters := 1 + g%3
		var sb strings.Builder
		for i := 0; i < n; i++ {
			sb.WriteByte(byte('a' + nextRandom(&seed)%letters))
		}
		strs = append(strs, sb.String())
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		groups := largeGroupPositions(strs[round%count])
		total += int64(len(groups))
		for _, g := range groups {
			checksum = (checksum*131 + g[0]*1009 + g[1]) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d strings: %d groups, checksum %d\n", rounds, count, total, checksum)
}
