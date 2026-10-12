// Benchmark for #425: mirror of word_squares.kara (a map of prefixes).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func extend(rows *[]string, length int, byPrefix map[string][]int, words []string, found *[][]string) {
	r := len(*rows)
	if r == length {
		square := make([]string, length)
		copy(square, *rows)
		*found = append(*found, square)
		return
	}
	prefix := make([]byte, 0, r)
	for _, row := range *rows {
		prefix = append(prefix, row[r])
	}
	for _, i := range byPrefix[string(prefix)] {
		*rows = append(*rows, words[i])
		extend(rows, length, byPrefix, words, found)
		*rows = (*rows)[:len(*rows)-1]
	}
}

func wordSquares(words []string) [][]string {
	length := len(words[0])
	byPrefix := make(map[string][]int)
	for i, word := range words {
		for k := 0; k < length; k++ {
			byPrefix[word[:k]] = append(byPrefix[word[:k]], i)
		}
	}
	found := [][]string{}
	rows := []string{}
	extend(&rows, length, byPrefix, words, &found)
	return found
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(seed *int64) string {
	word := make([]byte, 4)
	for k := range word {
		word[k] = byte('a' + step(seed)%16)
	}
	return string(word)
}

func main() {
	rounds := int64(20)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	n := int64(1000)
	seed := int64(425)
	seen := make(map[string]bool)
	words := []string{}
	for int64(len(words)) < n {
		word := randomWord(&seed)
		if !seen[word] {
			seen[word] = true
			words = append(words, word)
		}
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		word := randomWord(&seed)
		for seen[word] {
			word = randomWord(&seed)
		}
		at := r * 389 % n
		delete(seen, words[at])
		seen[word] = true
		words[at] = word
		squares := wordSquares(words)
		total += int64(len(squares))
		for _, square := range squares {
			checksum = (checksum*31 + int64(square[0][0]) + int64(square[3][3])) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d words: %d squares, checksum %d\n", rounds, n, total, checksum)
}
