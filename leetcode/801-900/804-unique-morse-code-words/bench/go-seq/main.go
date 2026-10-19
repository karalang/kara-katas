// LeetCode 804 -- Unique Morse Code Words: the bench, mirroring
// unique_morse.kara with the same set of strings.
package main

import (
	"fmt"
	"strings"
)

var codes = [26]string{".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--",
	"-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."}

var seed int64 = 804

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// morse is the word written in Morse code, its letters' codes run
// together.
func morse(word string) string {
	var out strings.Builder
	for i := 0; i < len(word); i++ {
		out.WriteString(codes[word[i]-97])
	}
	return out.String()
}

func uniqueMorseRepresentations(words []string) int64 {
	seen := make(map[string]struct{})
	for _, word := range words {
		seen[morse(word)] = struct{}{}
	}
	return int64(len(seen))
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	short := "etianm"
	lists := make([][]string, 0)
	for l := 0; l < 64; l++ {
		words := make([]string, 0)
		for w := 0; w < 100; w++ {
			length := 1 + nextRandom()%12
			few := nextRandom()%2 == 0
			word := make([]byte, 0)
			for k := int64(0); k < length; k++ {
				if few {
					word = append(word, short[nextRandom()%6])
				} else {
					word = append(word, letters[nextRandom()%26])
				}
			}
			words = append(words, string(word))
		}
		lists = append(lists, words)
	}
	var rounds int64 = 100000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		k := uniqueMorseRepresentations(lists[r%64])
		total += k
		check = (check*131 + k) % 1000000007
	}
	fmt.Printf("%d rounds of 100 words: %d codes in all, checksum %d\n", rounds, total, check)
}
