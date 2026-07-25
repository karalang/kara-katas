// Benchmark harness for LeetCode #290 — Word Pattern.
// Mirrors word_pattern.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"strings"
)

func splitWords(s string) []string {
	words := make([]string, 0)
	var cur []byte
	have := false
	for i := 0; i < len(s); i++ {
		b := s[i]
		if b == ' ' {
			if have {
				words = append(words, string(cur))
				cur = cur[:0]
				have = false
			}
		} else {
			cur = append(cur, b)
			have = true
		}
	}
	if have {
		words = append(words, string(cur))
	}
	return words
}

func wordPattern(pattern string, s string) bool {
	words := splitWords(s)
	if len(pattern) != len(words) {
		return false
	}

	p2w := make(map[int64]string)
	w2p := make(map[string]int64)

	for i := 0; i < len(pattern); i++ {
		c := int64(pattern[i])
		w := words[i]

		if prev, ok := p2w[c]; ok {
			if prev != w {
				return false
			}
		} else {
			p2w[c] = w
		}
		if pc, ok := w2p[w]; ok {
			if pc != c {
				return false
			}
		} else {
			w2p[w] = c
		}
	}
	return true
}

const (
	NP     = 8
	PL     = 1000
	AlphaN = 26
	Iters  = 2500
)

func main() {
	alpha := make([]string, AlphaN)
	for a := 0; a < AlphaN; a++ {
		alpha[a] = string(rune(97 + a))
	}

	patterns := make([]string, 0, NP)
	subjects := make([]string, 0, NP)
	for j := 0; j < NP; j++ {
		var pat strings.Builder
		var sub strings.Builder
		for i := 0; i < PL; i++ {
			slot := (i + j) % AlphaN
			pat.WriteString(alpha[slot])
			if i > 0 {
				sub.WriteByte(' ')
			}
			wslot := slot
			if j%2 == 1 && i == PL-1 {
				wslot = j % AlphaN
			}
			fmt.Fprintf(&sub, "w%d", wslot)
		}
		patterns = append(patterns, pat.String())
		subjects = append(subjects, sub.String())
	}

	var sink int64
	for it := 0; it < Iters; it++ {
		idx := (it * 3) % NP
		if wordPattern(patterns[idx], subjects[idx]) {
			sink += int64(it) + 1
		} else {
			sink++
		}
	}
	fmt.Println(sink)
}
