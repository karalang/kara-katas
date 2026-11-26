// LeetCode #1451 Rearrange Words in a Sentence: the bench, a mirror of
// arrange_words.kara.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func arrangeWords(text string) string {
	// the words lowered, sorted by length with ties kept in order by the
	// stable sort, joined, and the first letter raised
	words := strings.Split(strings.ToLower(text), " ")
	sort.SliceStable(words, func(i, j int) bool { return len(words[i]) < len(words[j]) })
	joined := strings.Join(words, " ")
	return strings.ToUpper(joined[:1]) + joined[1:]
}

func main() {
	// 200 texts of 15000 words of 1 to 10 letters, the constraints' most,
	// each arranged and its letters folded to a checksum
	var seed int64 = 1451
	var check int64 = 0
	for r := 0; r < 200; r++ {
		var text strings.Builder
		for i := 0; i < 15000; i++ {
			if i > 0 {
				text.WriteByte(' ')
			}
			seed = (seed*1103515245 + 12345) % 2147483648
			wl := 1 + seed/65536%10
			for j := int64(0); j < wl; j++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				c := byte('a' + seed/65536%26)
				if i == 0 && j == 0 {
					c -= 'a' - 'A'
				}
				text.WriteByte(c)
			}
		}
		out := arrangeWords(text.String())
		for i := 0; i < len(out); i++ {
			check = (check*131 + int64(out[i])) % 1000000007
		}
	}
	fmt.Printf("200 texts of 15000 words: checksum %d\n", check)
}
