// LeetCode #1839: Longest Substring Of All Vowels in Order -- the bench in Go: the ★ arm over
// 1000 calls on 40 words of 10^5 vowels, built once, each vowel the one
// before it again, the next vowel, an `a`, or any vowel, each call's word
// drawn from the checksum so far. The arm reads the word's bytes where they
// are, so no call copies one.
package main

import "fmt"

func longestBeautifulSubstring(word string) int64 {
	var best int64
	length, vowels := int64(1), int64(1)
	for i := 1; i < len(word); i++ {
		if word[i] < word[i-1] {
			length = 1
			vowels = 1
		} else {
			length++
			if word[i] > word[i-1] {
				vowels++
			}
		}
		if vowels == 5 {
			best = max(best, length)
		}
	}
	return best
}

func main() {
	seed := int64(1839)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	vowels := "aeiou"
	words := make([]string, 0, 40)
	for w := 0; w < 40; w++ {
		out := make([]byte, 0, 100000)
		var at int64
		for i := 0; i < 100000; i++ {
			roll := nextRandom() % 10
			if roll < 4 {
				// the same vowel again
			} else if roll < 8 {
				at = min(at+1, 4)
			} else if roll < 9 {
				at = 0
			} else {
				at = nextRandom() % 5
			}
			out = append(out, vowels[at])
		}
		words = append(words, string(out))
	}
	var check int64
	for call := int64(0); call < 1000; call++ {
		w := words[(check+call)%40]
		check = (check*31 + longestBeautifulSubstring(w)) % 1000000007
	}
	fmt.Printf("1000 calls: checksum %d\n", check)
}
