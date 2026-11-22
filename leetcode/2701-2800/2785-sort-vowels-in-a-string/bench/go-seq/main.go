// LeetCode #2785: Sort Vowels in a String -- the bench in Go: the ★ arm
// over 20 strings of 10^5 letters from all 52, all drawn first, then each
// answered 10 times.
package main

import (
	"fmt"
	"slices"
	"strings"
)

func isVowel(c rune) bool {
	switch c {
	case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U':
		return true
	}
	return false
}

func sortVowels(s string) string {
	var vowels []rune
	for _, c := range s {
		if isVowel(c) {
			vowels = append(vowels, c)
		}
	}
	slices.Sort(vowels)
	next := 0
	var out strings.Builder
	for _, c := range s {
		if isVowel(c) {
			out.WriteRune(vowels[next])
			next++
		} else {
			out.WriteRune(c)
		}
	}
	return out.String()
}

var seed int64 = 2785

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomText(n int64, from string) string {
	letters := []rune(from)
	out := make([]rune, n)
	for i := range out {
		out[i] = letters[nextRandom()%int64(len(letters))]
	}
	return string(out)
}

func main() {
	count := 20
	rounds := 10
	every := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	cases := make([]string, count)
	for c := range cases {
		cases[c] = randomText(100000, every)
	}
	var check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, s := range cases {
			t := sortVowels(s)
			for i := 0; i < len(t); i++ {
				check = (check*31 + int64(t[i])) % 1000000007
			}
			check = (check + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of 10^5, %d rounds: checksum %d\n", count, rounds, check)
}
