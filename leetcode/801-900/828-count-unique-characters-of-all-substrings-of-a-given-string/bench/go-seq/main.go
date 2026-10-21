// Benchmark for #828: Count Unique Characters of All Substrings of a Given
// String -- the ★ arm (each character's contribution).
//
// Mirrors unique_letter_string.kara: a character at i is unique in
// (i - prev) * (next - i) substrings, prev and next the copies of its
// letter beside it; one pass keeps the last two positions of each letter
// and settles the middle one each time a letter recurs.
package main

import (
	"fmt"
	"strings"
)

func uniqueLetterString(s string) int64 {
	n := int64(len(s))
	last := make([]int64, 26)
	before := make([]int64, 26)
	for c := range last {
		last[c], before[c] = -1, -1
	}
	var total int64
	for i := int64(0); i < n; i++ {
		c := int64(s[i] - 'A')
		if last[c] >= 0 {
			total += (last[c] - before[c]) * (i - last[c])
		}
		before[c] = last[c]
		last[c] = i
	}
	for c := 0; c < 26; c++ {
		if last[c] >= 0 {
			total += (last[c] - before[c]) * (n - last[c])
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = int64(32), int64(12800), 100000
	seed := int64(828)
	strs := make([]string, 0, count)
	for g := int64(0); g < count; g++ {
		letters := 1 + g%26
		var sb strings.Builder
		for i := 0; i < n; i++ {
			sb.WriteByte(byte('A' + nextRandom(&seed)%letters))
		}
		strs = append(strs, sb.String())
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		r := uniqueLetterString(strs[round%count])
		total += r
		checksum = (checksum*131 + r) % 1000000007
	}
	fmt.Printf("%d rounds of %d strings: total %d, checksum %d\n", rounds, count, total, checksum)
}
