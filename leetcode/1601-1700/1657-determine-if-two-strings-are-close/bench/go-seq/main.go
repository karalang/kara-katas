// LeetCode #1657: Determine if Two Strings Are Close -- the bench's Go
// mirror: the ★ arm on 400 random pairs of words of 100000 letters, each
// pair from the first 1 to 26 of the alphabet, half of the second words
// made close by construction, all drawn first.
package main

import (
	"fmt"
	"sort"
)

func closeStrings(word1, word2 string) bool {
	var count1, count2 [26]int64
	for i := 0; i < len(word1); i++ {
		count1[word1[i]-'a']++
	}
	for i := 0; i < len(word2); i++ {
		count2[word2[i]-'a']++
	}
	for i := 0; i < 26; i++ {
		if (count1[i] == 0) != (count2[i] == 0) {
			return false
		}
	}
	sort.Slice(count1[:], func(i, j int) bool { return count1[i] < count1[j] })
	sort.Slice(count2[:], func(i, j int) bool { return count2[i] < count2[j] })
	return count1 == count2
}

var seed int64 = 1657

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n int, letters int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%letters)
	}
	return string(b)
}

func main() {
	type pair struct{ word1, word2 string }
	pairs := make([]pair, 0, 400)
	for p := 0; p < 400; p++ {
		alphabet := nextRandom()%26 + 1
		word1 := randomWord(100000, alphabet)
		var word2 string
		if nextRandom()%2 == 0 {
			word2 = randomWord(100000, alphabet)
		} else {
			a := byte('a' + nextRandom()%alphabet)
			b := byte('a' + nextRandom()%alphabet)
			w := make([]byte, len(word1))
			for i := range w {
				c := word1[len(word1)-1-i]
				if c == a {
					c = b
				} else if c == b {
					c = a
				}
				w[i] = c
			}
			word2 = string(w)
		}
		pairs = append(pairs, pair{word1, word2})
	}
	var check, close int64
	for _, p := range pairs {
		answer := closeStrings(p.word1, p.word2)
		var v int64 = 1
		if answer {
			close++
			v = 2
		}
		check = (check*31 + v) % 1000000007
	}
	fmt.Printf("400 pairs of 100000 letters: %d close, checksum %d\n", close, check)
}
