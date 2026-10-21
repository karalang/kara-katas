// Benchmark for #819: Most Common Word -- the ★ arm (a map of counts).
//
// Mirrors most_common_word.kara: lower every letter and turn everything
// else into a space, count each word that is not banned in a map, and
// return the word counted most, the first alphabetically of two counted
// as often.
package main

import (
	"fmt"
	"strings"
)

func mostCommonWord(paragraph string, banned []string) string {
	cleaned := make([]byte, len(paragraph))
	for i := 0; i < len(paragraph); i++ {
		c := paragraph[i]
		switch {
		case c >= 'A' && c <= 'Z':
			cleaned[i] = c + 32
		case c >= 'a' && c <= 'z':
			cleaned[i] = c
		default:
			cleaned[i] = ' '
		}
	}
	ruledOut := make(map[string]bool, len(banned))
	for _, w := range banned {
		ruledOut[w] = true
	}
	counts := make(map[string]int64)
	for _, word := range strings.Fields(string(cleaned)) {
		if !ruledOut[word] {
			counts[word]++
		}
	}
	best := ""
	most := int64(0)
	for word, n := range counts {
		if n > most || (n == most && word < best) {
			best = word
			most = n
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(seed *int64) string {
	length := 1 + nextRandom(seed)%10
	b := make([]byte, length)
	for i := range b {
		b[i] = byte('a' + nextRandom(seed)%26)
	}
	return string(b)
}

func main() {
	count := 64
	rounds := int64(200000)
	seed := int64(819)
	marks := []string{" ", " ", " ", ", ", ". ", "! ", "? ", "; ", "' ", ","}
	vocabulary := make([]string, 300)
	for k := range vocabulary {
		vocabulary[k] = randomWord(&seed)
	}
	paragraphs := make([]string, 0, count)
	banned := make([][]string, 0, count)
	for g := 0; g < count; g++ {
		var p strings.Builder
		for p.Len() < 990 {
			a := nextRandom(&seed) % 300
			k := a * (nextRandom(&seed) % 300) / 300
			word := vocabulary[k]
			if nextRandom(&seed)%4 == 0 {
				word = strings.ToUpper(word)
			}
			p.WriteString(word)
			p.WriteString(marks[nextRandom(&seed)%10])
		}
		paragraphs = append(paragraphs, p.String())
		ruledOut := make([]string, 0, 100)
		for k := 0; k < 50; k++ {
			ruledOut = append(ruledOut, vocabulary[nextRandom(&seed)%30])
		}
		for k := 0; k < 50; k++ {
			ruledOut = append(ruledOut, randomWord(&seed))
		}
		banned = append(banned, ruledOut)
	}
	total := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % int64(count)
		answer := mostCommonWord(paragraphs[g], banned[g])
		total += int64(len(answer))
		for i := 0; i < len(answer); i++ {
			checksum = (checksum*131 + int64(answer[i])) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d paragraphs: total %d, checksum %d\n", rounds, count, total, checksum)
}
