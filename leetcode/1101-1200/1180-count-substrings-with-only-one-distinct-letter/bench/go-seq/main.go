// LeetCode #1180: Count Substrings with Only One Distinct Letter -- the ★
// arm's bench in Go: one pass, the run of equal letters ending at each
// position added at every step. The same strings and the same 100 rounds.
package main

import "fmt"

func countLetters(s string) int64 {
	total, run := int64(0), int64(0)
	last := byte(0)
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c == last {
			run++
		} else {
			run = 1
			last = c
		}
		total += run
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1180)
	strings := make([]string, 0, 1000)
	for i := 0; i < 1000; i++ {
		m := 1 + nextRandom(&seed)%4
		b := make([]byte, 1000)
		for j := range b {
			b[j] = byte('a' + nextRandom(&seed)%m)
		}
		strings = append(strings, string(b))
	}
	rounds := 100
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			check = (check*131 + countLetters(s)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 1000 strings: checksum %d\n", rounds, check)
}
