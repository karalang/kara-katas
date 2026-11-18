// LeetCode #2273: Find Resultant Array After Removing Anagrams -- the
// bench, the ★ arm.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func sortedLetters(word string) string {
	letters := []rune(word)
	sort.Slice(letters, func(a, b int) bool { return letters[a] < letters[b] })
	return string(letters)
}

func removeAnagrams(words []string) []string {
	kept := []string{}
	last := ""
	for _, w := range words {
		key := sortedLetters(w)
		if len(kept) == 0 || key != last {
			kept = append(kept, w)
		}
		last = key
	}
	return kept
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2273

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 20000; t++ {
		words := make([]string, 0, 100)
		for i := 0; i < 100; i++ {
			if i > 0 && nextRandom()%2 == 0 {
				letters := []byte(words[i-1])
				for j := 9; j >= 1; j-- {
					r := nextRandom() % int64(j+1)
					letters[j], letters[r] = letters[r], letters[j]
				}
				words = append(words, string(letters))
			} else {
				var b strings.Builder
				for j := 0; j < 10; j++ {
					b.WriteByte(byte('a' + nextRandom()%4))
				}
				words = append(words, b.String())
			}
		}
		kept := removeAnagrams(words)
		check = (check*31 + int64(len(kept))*1000 + int64(kept[len(kept)-1][0])) % 1000000007
	}
	fmt.Printf("20000 lists of 100: checksum %d\n", check)
}
