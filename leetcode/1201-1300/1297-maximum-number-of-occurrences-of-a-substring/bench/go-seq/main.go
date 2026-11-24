// LeetCode #1297 bench: the ★ arm (one window of minSize letters slid along
// the string, each with few enough distinct letters counted in a map by its
// text) over 10 strings of 10^5 letters over the first 2 to 6 letters, built
// once; then 20 passes, each setting one letter of every string and its limits
// from the checksum so far, answering it, and folding the answer into the
// checksum.
package main

import "fmt"

func maxFreq(s string, maxLetters, minSize, maxSize int64) int64 {
	n := int64(len(s))
	letters := make([]int64, 26)
	var distinct int64
	seen := map[string]int64{}
	var best int64
	for i := int64(0); i < n; i++ {
		add := s[i] - 97
		if letters[add] == 0 {
			distinct++
		}
		letters[add]++
		if i >= minSize {
			gone := s[i-minSize] - 97
			letters[gone]--
			if letters[gone] == 0 {
				distinct--
			}
		}
		if i+1 >= minSize && distinct <= maxLetters {
			window := s[i+1-minSize : i+1]
			times := seen[window] + 1
			seen[window] = times
			if times > best {
				best = times
			}
		}
	}
	return best
}

var seed int64 = 1297

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	texts := [][]byte{}
	for t := int64(0); t < 10; t++ {
		alphabet := 2 + t%5
		text := make([]byte, 0, 100000)
		for j := 0; j < 100000; j++ {
			text = append(text, byte(97+nextRandom()%alphabet))
		}
		texts = append(texts, text)
	}
	var check int64
	for p := int64(0); p < 20; p++ {
		for t := range texts {
			texts[t][check%100000] = byte(97 + check%(2+int64(t)%5))
			s := string(texts[t])
			minSize := 1 + check%26
			maxLetters := 1 + (check/26)%26
			check = (check*31 + maxFreq(s, maxLetters, minSize, minSize) + p) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 strings of 10^5: checksum %d\n", check)
}
