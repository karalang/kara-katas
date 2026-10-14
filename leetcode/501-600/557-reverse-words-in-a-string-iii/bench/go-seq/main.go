// Benchmark for #557: Go mirror of the ★ arm (split, reverse, join); see
// ../reverse_words_in_a_string_iii.kara.
package main

import (
	"fmt"
	"strings"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func reverseWords(s string) string {
	words := []string{}
	for _, w := range strings.Split(s, " ") {
		r := []rune(w)
		for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
			r[i], r[j] = r[j], r[i]
		}
		words = append(words, string(r))
	}
	return strings.Join(words, " ")
}

func main() {
	count := 100
	seed := int64(557)
	texts := []string{}
	words := 0
	for i := 0; i < count; i++ {
		var sb strings.Builder
		for sb.Len() < 49980 {
			if sb.Len() > 0 {
				sb.WriteByte(' ')
			}
			length := 1 + nextRandom(&seed)%12
			for k := int64(0); k < length; k++ {
				sb.WriteByte(byte('!' + nextRandom(&seed)%94))
			}
			words++
		}
		texts = append(texts, sb.String())
	}
	var checksum int64
	for round := 0; round < 50; round++ {
		for g := 0; g < count; g++ {
			b := reverseWords(texts[(round*7+g)%count])
			checksum = (checksum*31 + int64(len(b)) + int64(b[0])*7 + int64(b[len(b)/2])) % 1000000007
		}
	}
	fmt.Printf("%d texts, %d words, 50 rounds each: checksum %d\n", count, words, checksum)
}
