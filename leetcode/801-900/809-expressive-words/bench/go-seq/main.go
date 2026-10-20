// LeetCode 809 -- Expressive Words: the bench, with the ★ arm's two
// pointers over the groups.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 809

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func stretchy(s, word string) bool {
	i, j := 0, 0
	for i < len(s) && j < len(word) {
		c := s[i]
		if word[j] != c {
			return false
		}
		fromI := i
		for i < len(s) && s[i] == c {
			i++
		}
		fromJ := j
		for j < len(word) && word[j] == c {
			j++
		}
		inS, inWord := i-fromI, j-fromJ
		if inS < inWord || (inS > inWord && inS < 3) {
			return false
		}
	}
	return i == len(s) && j == len(word)
}

func expressiveWords(s string, words []string) int64 {
	var count int64
	for _, w := range words {
		if stretchy(s, w) {
			count++
		}
	}
	return count
}

type group struct {
	c byte
	n int64
}

func spell(groups []group) string {
	var b strings.Builder
	for _, g := range groups {
		for k := int64(0); k < g.n; k++ {
			b.WriteByte(g.c)
		}
	}
	return b.String()
}

func main() {
	texts := []string{}
	lists := [][]string{}
	for k := 0; k < 64; k++ {
		groups := []group{}
		last := int64(26)
		for g := 0; g < 25; g++ {
			c := nextRandom() % 5
			if c == last {
				c = (c + 1) % 5
			}
			last = c
			groups = append(groups, group{byte(97 + c), 1 + nextRandom()%4})
		}
		words := []string{}
		for w := 0; w < 100; w++ {
			if nextRandom()%4 == 0 {
				n := 1 + nextRandom()%100
				var b strings.Builder
				for i := int64(0); i < n; i++ {
					b.WriteByte(byte(97 + nextRandom()%5))
				}
				words = append(words, b.String())
			} else {
				shrunk := []group{}
				for _, g := range groups {
					n := g.n
					if n >= 3 {
						n = 1 + nextRandom()%g.n
					}
					shrunk = append(shrunk, group{g.c, n})
				}
				if nextRandom()%3 == 0 {
					g := nextRandom() % 25
					shrunk[g].n = groups[g].n + 1
				}
				words = append(words, spell(shrunk))
			}
		}
		texts = append(texts, spell(groups))
		lists = append(lists, words)
	}
	rounds := int64(200000)
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		n := expressiveWords(texts[r%64], lists[r%64])
		total += n
		check = (check*131 + n + r) % 1000000007
	}
	fmt.Printf("%d rounds of 100 words: %d stretchy, checksum %d\n", rounds, total, check)
}
