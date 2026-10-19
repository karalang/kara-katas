// LeetCode 763 — Partition Labels: benchmark, the ★ arm in Go.
// 100,000 random strings of 500 letters.
package main

import (
	"fmt"
	"strings"
)

func partitionLabels(s string) []int64 {
	var last [26]int64
	for i := 0; i < len(s); i++ {
		last[s[i]-'a'] = int64(i)
	}
	var sizes []int64
	var start, end int64
	for i := 0; i < len(s); i++ {
		if last[s[i]-'a'] > end {
			end = last[s[i]-'a']
		}
		if int64(i) == end {
			sizes = append(sizes, end-start+1)
			start = int64(i) + 1
		}
	}
	return sizes
}

var seed int64 = 763

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 100000
	letters := "abcdefghijklmnopqrstuvwxyz"
	var parts, check int64
	for r := 0; r < rounds; r++ {
		width := 1 + nextRandom()%4
		var b strings.Builder
		for i := int64(0); i < 500; i++ {
			k := min(i*26/500+nextRandom()%width, 25)
			b.WriteString(letters[k : k+1])
		}
		sizes := partitionLabels(b.String())
		parts += int64(len(sizes))
		for _, size := range sizes {
			check = (check*31 + size) % 1000000007
		}
	}
	fmt.Printf("%d strings of 500 letters: %d parts, checksum %d\n", rounds, parts, check)
}
