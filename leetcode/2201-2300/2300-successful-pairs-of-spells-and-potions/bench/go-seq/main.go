// LeetCode #2300: Successful Pairs of Spells and Potions -- the bench,
// the ★ arm in Go. Sort a copy of the potions, then for each spell
// binary-search the first potion whose product with it reaches success.
package main

import (
	"fmt"
	"sort"
)

func successfulPairs(spells, potions []int64, success int64) []int64 {
	sorted := append([]int64(nil), potions...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i] < sorted[j] })
	m := int64(len(sorted))
	out := make([]int64, 0, len(spells))
	for _, spell := range spells {
		lo, hi := int64(0), m
		for lo < hi {
			mid := (lo + hi) / 2
			if spell*sorted[mid] < success {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		out = append(out, m-lo)
	}
	return out
}

var seed int64 = 2300

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	spells := make([][]int64, 10)
	potions := make([][]int64, 10)
	for c := 0; c < 10; c++ {
		s := make([]int64, 100000)
		p := make([]int64, 100000)
		for i := 0; i < 100000; i++ {
			hi := nextRandom()
			s[i] = (hi*32768+nextRandom())%100000 + 1
			hi = nextRandom()
			p[i] = (hi*32768+nextRandom())%100000 + 1
		}
		spells[c] = s
		potions[c] = p
	}
	var check int64
	for pass := int64(0); pass < 5; pass++ {
		for c := int64(0); c < 10; c++ {
			for _, x := range successfulPairs(spells[c], potions[c], 1000000000*c+7+pass) {
				check = (check*31 + x) % 1000000007
			}
		}
	}
	fmt.Printf("5 passes over 10 cases of 10^5 spells and potions: checksum %d\n", check)
}
