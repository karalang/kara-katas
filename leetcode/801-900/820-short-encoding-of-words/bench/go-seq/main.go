// Benchmark for #820: Short Encoding of Words -- the ★ arm (a set of the words).
//
// Mirrors short_encoding.kara: put every word in a set, take out every
// proper suffix of every word, and the words left each cost their length
// and a '#'.
package main

import "fmt"

func minimumLengthEncoding(words []string) int64 {
	kept := make(map[string]struct{})
	for _, word := range words {
		kept[word] = struct{}{}
	}
	for _, word := range words {
		for k := 1; k < len(word); k++ {
			delete(kept, word[k:])
		}
	}
	var total int64
	for word := range kept {
		total += int64(len(word)) + 1
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(seed *int64, letters, longest int64) string {
	length := 1 + nextRandom(seed)%longest
	word := make([]byte, 0, length)
	for i := int64(0); i < length; i++ {
		word = append(word, byte('a'+nextRandom(seed)%letters))
	}
	return string(word)
}

func main() {
	count := 64
	rounds := 12000
	seed := int64(820)
	lists := make([][]string, 0, count)
	for i := 0; i < count; i++ {
		words := make([]string, 0, 2000)
		for j := 0; j < 2000; j++ {
			words = append(words, randomWord(&seed, 5, 7))
		}
		lists = append(lists, words)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		answer := minimumLengthEncoding(lists[round%count])
		total += answer
		checksum = (checksum*131 + answer) % 1000000007
	}
	fmt.Printf("%d rounds of %d lists of 2000 words: total %d, checksum %d\n", rounds, count, total, checksum)
}
