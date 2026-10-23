// LeetCode #890 bench: Go mirror of find_and_replace_pattern.kara (the
// table arm, two tables of 26 letters) on the same 6000 words.
package main

import "fmt"

func findAndReplacePattern(words []string, pattern string) []string {
	out := []string{}
	for _, word := range words {
		if matches(word, pattern) {
			out = append(out, word)
		}
	}
	return out
}

func matches(word, pattern string) bool {
	var to, from [26]int64
	for i := range to {
		to[i] = -1
		from[i] = -1
	}
	for i := 0; i < len(pattern); i++ {
		a := int64(pattern[i] - 97)
		b := int64(word[i] - 97)
		if to[a] < 0 && from[b] < 0 {
			to[a] = b
			from[b] = a
		} else if to[a] != b || from[b] != a {
			return false
		}
	}
	return true
}

var seed int64 = 890

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	words := make([]string, 0, 6000)
	for k := 0; k < 6000; k++ {
		w := make([]byte, 10)
		for i := range w {
			w[i] = byte(97 + nextRandom()%3)
		}
		words = append(words, string(w))
	}
	found, check := 0, 0
	for k := range words {
		kept := findAndReplacePattern(words, words[k])
		found += len(kept)
		check = (check*131 + len(kept)) % 1000000007
	}
	fmt.Printf("6000 patterns over 6000 words of 10 letters: %d matches, checksum %d\n", found, check)
}
