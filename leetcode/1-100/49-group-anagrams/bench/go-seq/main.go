// LeetCode 49 — sorted-key Group Anagrams, Go single-threaded mirror.
// Algorithmic peer of bench/group_anagrams.{kara,rs,c,py}. Same deterministic
// input: N=20_000 words of length L=8 from G=1_000 classes (letters are L
// consecutive alphabet letters mod 26, so 26 distinct anagram groups). K=40
// outer iterations. Stdout sink: K * 26 = 1040.
package main

import (
	"fmt"
	"sort"
)

const alphabet = "abcdefghijklmnopqrstuvwxyz"

func countGroups(words []string) int64 {
	indexOf := make(map[string]int64)
	var groups int64
	for _, w := range words {
		b := []byte(w)
		sort.Slice(b, func(i, j int) bool { return b[i] < b[j] })
		key := string(b)
		if _, ok := indexOf[key]; !ok {
			indexOf[key] = groups
			groups++
		}
	}
	return groups
}

func makeWords(n, g, l int64) []string {
	words := make([]string, 0, n)
	for i := int64(0); i < n; i++ {
		grp := i % g
		rot := (i / g) % l
		seed := make([]byte, l)
		for k := int64(0); k < l; k++ {
			seed[k] = alphabet[(grp+k)%26]
		}
		word := make([]byte, 0, l)
		word = append(word, seed[rot:l]...)
		word = append(word, seed[0:rot]...)
		words = append(words, string(word))
	}
	return words
}

func main() {
	words := makeWords(20000, 1000, 8)
	var total int64
	for it := 0; it < 40; it++ {
		total += countGroups(words)
	}
	fmt.Println(total)
}
