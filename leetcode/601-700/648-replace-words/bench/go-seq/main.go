// LeetCode #648: Replace Words -- Go mirror of the Kāra bench.
//
// The ★ arm over the same inputs and rounds: a trie of the roots as a
// slice of 26-entry child tables, each word walked until the first root
// ends, the words split on spaces and joined back.
package main

import (
	"fmt"
	"strings"
)

func replaceWords(dictionary []string, sentence string) string {
	next := [][]int{make([]int, 26)}
	ends := []bool{false}
	for _, root := range dictionary {
		node := 0
		for i := 0; i < len(root); i++ {
			c := int(root[i] - 'a')
			if next[node][c] == 0 {
				next[node][c] = len(next)
				next = append(next, make([]int, 26))
				ends = append(ends, false)
			}
			node = next[node][c]
		}
		ends[node] = true
	}
	var out []string
	for _, word := range strings.Split(sentence, " ") {
		node := 0
		length := 0
		for length < len(word) && !ends[node] {
			node = next[node][word[length]-'a']
			if node == 0 {
				break
			}
			length++
		}
		if node != 0 && ends[node] {
			out = append(out, word[:length])
		} else {
			out = append(out, word)
		}
	}
	return strings.Join(out, " ")
}

var seed int64 = 648

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(shortest, longest, letters int64) string {
	n := shortest + nextRandom()%(longest-shortest+1)
	var b strings.Builder
	for i := int64(0); i < n; i++ {
		b.WriteByte(byte(97 + nextRandom()%letters))
	}
	return b.String()
}

func main() {
	const inputs = 20
	const rounds = 100
	var dictionaries [][]string
	var sentences []string
	for i := 0; i < inputs; i++ {
		letters := 3 + nextRandom()%6
		roots := make([]string, 0, 1000)
		for j := 0; j < 1000; j++ {
			roots = append(roots, randomWord(3, 6, letters))
		}
		words := make([]string, 0, 20000)
		for j := 0; j < 20000; j++ {
			words = append(words, randomWord(1, 10, letters))
		}
		dictionaries = append(dictionaries, roots)
		sentences = append(sentences, strings.Join(words, " "))
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		i := (r * 7) % inputs
		out := replaceWords(dictionaries[i], sentences[i])
		for j := 0; j < len(out); j++ {
			total++
			checksum = (checksum*31 + int64(out[j])) % 1000000007
		}
	}
	fmt.Printf("%d inputs, %d rounds: %d characters, checksum %d\n", inputs, rounds, total, checksum)
}
