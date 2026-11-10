// LeetCode #2068: Check Whether Two Strings are Almost Equivalent -- Go
// mirror of the ★ arm's benchmark (almost.kara): every pair of 1500 words
// of 100 letters, each a common word of `a`, `b` and `c` with up to 30
// letters changed.
package main

import "fmt"

func checkAlmostEquivalent(word1, word2 string) bool {
	var diff [26]int64
	for i := 0; i < len(word1); i++ {
		diff[word1[i]-'a']++
	}
	for i := 0; i < len(word2); i++ {
		diff[word2[i]-'a']--
	}
	for _, d := range diff {
		if d > 3 || d < -3 {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	letters := []byte("abc")
	seed := int64(2068)
	base := make([]byte, 100)
	for i := range base {
		base[i] = letters[nextRandom(&seed)%3]
	}
	words := make([]string, 0, 1500)
	for w := 0; w < 1500; w++ {
		word := append([]byte(nil), base...)
		changes := nextRandom(&seed) % 31
		for k := int64(0); k < changes; k++ {
			i := nextRandom(&seed) % 100
			word[i] = letters[nextRandom(&seed)%3]
		}
		words = append(words, string(word))
	}
	yes, check := int64(0), int64(0)
	for i := int64(0); i < 1500; i++ {
		for j := i + 1; j < 1500; j++ {
			if checkAlmostEquivalent(words[i], words[j]) {
				yes++
				check = (check*31 + i*1500 + j) % 1000000007
			}
		}
	}
	fmt.Printf("1124250 pairs: %d almost equivalent, checksum %d\n", yes, check)
}
