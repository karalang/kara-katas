// Benchmark for #500: Go mirror of the ★ arm (a row number for every
// letter); see ../keyboard_row.kara. Each word is lower-cased into a
// fresh string, as the Kāra one is.
package main

import (
	"fmt"
	"strings"
)

func findWords(words []string) []string {
	rows := []string{"qwertyuiop", "asdfghjkl", "zxcvbnm"}
	var rowOf [26]int64
	for r := 0; r < 3; r++ {
		for _, ch := range rows[r] {
			rowOf[ch-'a'] = int64(r)
		}
	}
	var out []string
	for _, word := range words {
		first := int64(-1)
		oneRow := true
		for _, ch := range strings.ToLower(word) {
			r := rowOf[ch-'a']
			if first < 0 {
				first = r
			} else if r != first {
				oneRow = false
				break
			}
		}
		if oneRow {
			out = append(out, word)
		}
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 20,000 lists of 20 words of 1 to 100 letters, each word from one
	// row (2 in 3) or the whole alphabet, a letter upper case with odds
	// 1 in 4, built once. Then each list is solved once.
	pools := []string{"qwertyuiop", "asdfghjkl", "zxcvbnm", "abcdefghijklmnopqrstuvwxyz"}
	lists := 20000
	seed := int64(500)
	all := make([][]string, 0, lists)
	for l := 0; l < lists; l++ {
		words := make([]string, 0, 20)
		for w := 0; w < 20; w++ {
			var pool int64
			if nextRandom(&seed)%3 == 0 {
				pool = 3
			} else {
				pool = nextRandom(&seed) % 3
			}
			length := 1 + nextRandom(&seed)%100
			var b strings.Builder
			for i := int64(0); i < length; i++ {
				p := pools[pool]
				ch := p[nextRandom(&seed)%int64(len(p))]
				if nextRandom(&seed)%4 == 0 {
					b.WriteByte(ch - 'a' + 'A')
				} else {
					b.WriteByte(ch)
				}
			}
			words = append(words, b.String())
		}
		all = append(all, words)
	}
	kept, letters, checksum := int64(0), int64(0), int64(0)
	for k := 0; k < lists; k++ {
		for _, word := range findWords(all[k]) {
			kept++
			letters += int64(len(word))
			checksum = (checksum*31 + int64(len(word)) + int64(word[0])) % 1000000007
		}
	}
	fmt.Printf("%d lists of 20 words: %d words kept, %d letters, checksum %d\n", lists, kept, letters, checksum)
}
