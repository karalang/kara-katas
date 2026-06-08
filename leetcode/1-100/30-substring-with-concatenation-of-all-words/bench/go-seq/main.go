// LeetCode 30 — substring with concatenation of all words, Go seq mirror.
//
// Algorithmic mirror of concat_words.kara: same vocabulary, glibc LCG (high
// bits for the vocab pick), NSLOTS / RUNS, O(n) sliding-window search, and
// sink. Keys are `string` slices of the text (Go strings are immutable byte
// views, so slicing does not copy).
package main

import (
	"fmt"
	"strings"
)

func findSubstring(s string, words []string) []int64 {
	result := []int64{}
	k := len(words)
	if k == 0 {
		return result
	}
	wl := len(words[0])
	total := wl * k
	n := len(s)
	if wl == 0 || total > n {
		return result
	}

	need := make(map[string]int64)
	for _, w := range words {
		need[w]++
	}

	for r := 0; r < wl; r++ {
		seen := make(map[string]int64)
		var count int64 = 0
		left := r
		j := r
		for j+wl <= n {
			piece := s[j : j+wl]
			req, ok := need[piece]
			if !ok {
				seen = make(map[string]int64)
				count = 0
				left = j + wl
			} else {
				seen[piece]++
				count++
				for seen[piece] > req {
					lw := s[left : left+wl]
					seen[lw]--
					left += wl
					count--
				}
				if count == int64(k) {
					result = append(result, int64(left))
					lw := s[left : left+wl]
					seen[lw]--
					left += wl
					count--
				}
			}
			j += wl
		}
	}
	return result
}

func main() {
	const nslots = 50000
	const runs = 40

	chars := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"
	vocab := make([]string, 16)
	for v := 0; v < 16; v++ {
		vocab[v] = chars[v*4 : v*4+4]
	}

	var sb strings.Builder
	var state int64 = 1
	for t := 0; t < nslots; t++ {
		state = (state*1103515245 + 12345) % 2147483648
		v := (state / 131072) % 16
		sb.WriteString(vocab[int(v)])
	}
	s := sb.String()

	var sink int64 = 0
	for run := 0; run < runs; run++ {
		start := run % 13
		wordsR := make([]string, 4)
		for d := 0; d < 4; d++ {
			wordsR[d] = vocab[start+d]
		}
		res := findSubstring(s, wordsR)
		sink += int64(len(res))
		for _, idx := range res {
			sink += idx
		}
	}

	fmt.Println(sink)
}
