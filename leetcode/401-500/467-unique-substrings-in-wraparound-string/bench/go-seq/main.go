// Benchmark for #467: mirror of unique_substrings.kara (the ★ arm: the
// longest run ending at each letter) on the same workload.
package main

import (
	"fmt"
	"strings"
)

func findSubstringInWraproundString(s string) int64 {
	var longest [26]int64
	var run int64
	previous := int64(-1)
	for _, c := range s {
		code := int64(c) - 97
		if previous >= 0 && code == (previous+1)%26 {
			run++
		} else {
			run = 1
		}
		if run > longest[code] {
			longest[code] = run
		}
		previous = code
	}
	var total int64
	for _, length := range longest {
		total += length
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(i int64) rune {
	return rune(97 + i%26)
}

func main() {
	const count = 10
	const n = 100000
	const rounds = 100
	seed := int64(467)
	strs := make([]string, 0, count)
	for k := 0; k < count; k++ {
		var b strings.Builder
		last := nextRandom(&seed) % 26
		b.WriteRune(letter(last))
		for i := 1; i < n; i++ {
			if nextRandom(&seed)%16 == 0 {
				last = nextRandom(&seed) % 26
			} else {
				last = (last + 1) % 26
			}
			b.WriteRune(letter(last))
		}
		strs = append(strs, b.String())
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for k := 0; k < count; k++ {
			strs[k] += string(letter(nextRandom(&seed) % 26))
			found := findSubstringInWraproundString(strs[k])
			total += found
			checksum = (checksum*31 + found) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d strings: %d substrings in all, checksum %d\n", rounds, count, total, checksum)
}
