// LeetCode #1573: Number of Ways to Split a String -- bench: the ★ arm (the
// two gaps between the ones multiplied) over 20 strings of 500000
// characters, each with its own odds of a '1' from 1 in 1 to 1 in 1000,
// built once; then 10 rounds answering all 20, 200 answers.
package main

import (
	"fmt"
	"strings"
)

func numWays(s string) int64 {
	const m = 1000000007
	var ones []int64
	for i, c := range s {
		if c == '1' {
			ones = append(ones, int64(i))
		}
	}
	n := int64(len(s))
	t := len(ones)
	if t == 0 {
		return (n - 1) * (n - 2) / 2 % m
	}
	if t%3 != 0 {
		return 0
	}
	k := t / 3
	return (ones[k] - ones[k-1]) * (ones[2*k] - ones[2*k-1]) % m
}

var seed int64 = 1573

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	const n = 500000
	strs := make([]string, 0, 20)
	for v := 0; v < 20; v++ {
		odds := nextRandom()%1000 + 1
		var b strings.Builder
		for i := 0; i < n; i++ {
			if nextRandom()%odds == 0 {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		strs = append(strs, b.String())
	}
	var check, total int64
	for r := 0; r < 10; r++ {
		for _, s := range strs {
			ways := numWays(s)
			total += ways
			check = mix(check, ways)
		}
	}
	fmt.Printf("200 answers over 20 strings of %d characters: ways total %d, checksum %d\n", n, total, check)
}
