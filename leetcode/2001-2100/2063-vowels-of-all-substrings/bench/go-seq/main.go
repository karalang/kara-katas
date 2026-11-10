// LeetCode #2063: Vowels of All Substrings -- Go mirror of the ★ arm's
// benchmark (vowels.kara): one text of 140000 letters, each a vowel with
// chance 40 in 100, and 200 windows of 100000 letters cut from it at a
// random place among its first 32768, each copied out and answered on its
// own.
package main

import (
	"fmt"
	"strings"
)

func countVowels(word string) int64 {
	n := int64(len(word))
	total := int64(0)
	i := int64(0)
	for _, c := range word {
		if strings.ContainsRune("aeiou", c) {
			total += (i + 1) * (n - i)
		}
		i++
	}
	return total
}

var seed int64 = 2063

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	vowels := "aeiou"
	others := "bcdxyz"
	var b strings.Builder
	for k := 0; k < 140000; k++ {
		if nextRandom()%100 < 40 {
			b.WriteByte(vowels[nextRandom()%5])
		} else {
			b.WriteByte(others[nextRandom()%6])
		}
	}
	text := b.String()
	check := int64(0)
	for t := 0; t < 200; t++ {
		start := nextRandom()
		window := strings.Clone(text[start : start+100000])
		a := countVowels(window)
		check = (check*31 + a%1000000007) % 1000000007
	}
	fmt.Printf("200 windows: checksum %d\n", check)
}
