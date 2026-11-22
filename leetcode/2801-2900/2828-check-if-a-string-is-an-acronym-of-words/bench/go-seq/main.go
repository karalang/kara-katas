// LeetCode #2828: Check if a String Is an Acronym of Words -- the bench's
// Go mirror of the ★ arm: the lengths first, then every word's first
// byte against s's byte at the same place.
package main

import "fmt"

func isAcronym(words []string, s string) bool {
	if len(words) != len(s) {
		return false
	}
	for i, w := range words {
		if w[0] != s[i] {
			return false
		}
	}
	return true
}

var seed int64 = 2828

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word() string {
	n := nextRandom()%10 + 1
	b := make([]byte, n)
	for i := range b {
		b[i] = byte(97 + nextRandom()%3)
	}
	return string(b)
}

func main() {
	count, rounds := 20000, 100
	words := make([][]string, count)
	ss := make([]string, count)
	for c := 0; c < count; c++ {
		words[c] = make([]string, 100)
		for i := range words[c] {
			words[c][i] = word()
		}
		s := make([]byte, 100)
		for i := range s {
			s[i] = words[c][i][0]
		}
		if nextRandom()%4 == 0 {
			at := nextRandom() % 100
			s[at] = byte(97 + nextRandom()%3)
		}
		ss[c] = string(s)
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			bit := int64(0)
			if isAcronym(words[c], ss[c]) {
				yes++
				bit = 1
			}
			check = (check*31 + bit + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d cases of 100 words, %d rounds: %d true, checksum %d\n", count, rounds, yes, check)
}
