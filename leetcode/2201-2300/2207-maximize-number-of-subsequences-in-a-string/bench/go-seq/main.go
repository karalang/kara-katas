// benchmark's Go mirror of subsequences.kara (LeetCode #2207, the ★ arm):
// one pass counting the first letter so far, each second letter adding
// that count, then the more common letter added. The text is read rune
// by rune, as Kāra's `chars()`.
package main

import "fmt"

func maximumSubsequenceCount(text string, pattern string) int64 {
	p := []rune(pattern)
	first, second := p[0], p[1]
	var firsts, seconds, pairs int64
	for _, ch := range text {
		if ch == second {
			pairs += firsts
			seconds++
		}
		if ch == first {
			firsts++
		}
	}
	if firsts > seconds {
		return pairs + firsts
	}
	return pairs + seconds
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(n int, letters int64, seed *int64) string {
	w := make([]byte, n)
	for i := range w {
		w[i] = byte(97 + nextRandom(seed)%letters)
	}
	return string(w)
}

func main() {
	seed := int64(2207)
	sizes := []int64{2, 3, 26}
	texts := []string{}
	for t := 0; t < 12; t++ {
		texts = append(texts, randomWord(100000, sizes[t%3], &seed))
	}
	// each pass asks every text about its own pattern
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for t := int64(0); t < 12; t++ {
			letters := sizes[t%3]
			pattern := string([]byte{byte(97 + p%letters), byte(97 + (p*7+t)%letters)})
			check = (check*31 + maximumSubsequenceCount(texts[t], pattern)) % 1000000007
		}
	}
	fmt.Printf("50 passes over 12 texts: checksum %d\n", check)
}
