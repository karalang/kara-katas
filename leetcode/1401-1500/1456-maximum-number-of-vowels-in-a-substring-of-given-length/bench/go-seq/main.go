// LeetCode #1456 bench mirror: a window of k letters slid along the
// string, its vowels counted as a letter comes in and another goes out.
package main

import (
	"fmt"
	"strings"
)

func maxVowels(s string, k int32) int32 {
	letters := []rune(s)
	isVowel := func(c rune) bool { return strings.ContainsRune("aeiou", c) }
	var count int32
	for i := 0; i < int(k); i++ {
		if isVowel(letters[i]) {
			count++
		}
	}
	best := count
	for i := int(k); i < len(letters); i++ {
		if isVowel(letters[i]) {
			count++
		}
		if isVowel(letters[i-int(k)]) {
			count--
		}
		if count > best {
			best = count
		}
	}
	return best
}

func main() {
	// 200 strings of 10^5 letters, a vowel one time in 3, drawn once, each
	// asked for windows of 1 to 10^5 letters 5 times, the answers folded to
	// a checksum
	var seed int64 = 1456
	vowels := []rune("aeiou")
	others := []rune("bcdfghjklmnpqrstvwxyz")
	texts := make([]string, 0, 200)
	for t := 0; t < 200; t++ {
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			odd := seed/65536%3 == 0
			seed = (seed*1103515245 + 12345) % 2147483648
			pick := seed / 65536
			if odd {
				b.WriteRune(vowels[pick%5])
			} else {
				b.WriteRune(others[pick%21])
			}
		}
		texts = append(texts, b.String())
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, s := range texts {
			seed = (seed*1103515245 + 12345) % 2147483648
			k := 1 + seed/65536%100000
			check = (check*131 + int64(maxVowels(s, int32(k)))) % 1000000007
		}
	}
	fmt.Printf("1000 windows of 10^5 letters: checksum %d\n", check)
}
