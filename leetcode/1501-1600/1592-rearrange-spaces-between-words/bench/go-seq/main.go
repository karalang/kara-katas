// LeetCode #1592: Rearrange Spaces Between Words -- the bench in Go,
// mirroring spaces.kara.
package main

import (
	"fmt"
	"strings"
)

func reorderSpaces(text string) string {
	words := strings.Fields(text)
	spaces := strings.Count(text, " ")
	gaps := len(words) - 1
	if gaps == 0 {
		return words[0] + strings.Repeat(" ", spaces)
	}
	return strings.Join(words, strings.Repeat(" ", spaces/gaps)) + strings.Repeat(" ", spaces%gaps)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(n int64, seed *int64) string {
	b := make([]byte, n)
	for i := range b {
		r := nextRandom(seed) % 6
		if r < 2 {
			b[i] = ' '
		} else {
			b[i] = byte('a' + (r-2)%3)
		}
	}
	hi := nextRandom(seed)
	b[(hi*32768+nextRandom(seed))%n] = 'a'
	return string(b)
}

func main() {
	seed := int64(1592)
	texts := make([]string, 0)
	for t := 0; t < 200; t++ {
		texts = append(texts, draw(100000, &seed))
	}
	var check, trailing int64
	for _, text := range texts {
		answer := reorderSpaces(text)
		trailing += int64(len(answer) - len(strings.TrimRight(answer, " ")))
		for i := 0; i < len(answer); i++ {
			check = (check*31 + int64(answer[i]) + 1) % 1000000007
		}
	}
	fmt.Printf("200 texts of 100000 characters: %d trailing spaces, checksum %d\n", trailing, check)
}
