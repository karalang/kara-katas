// Benchmark harness for LeetCode #127 — Word Ladder.
// Mirrors word_ladder.kara algorithm-for-algorithm.
//
// Go's map[string]int hashes with an AES-NI-based function it does not let you
// swap, so this lane is neither the default-SipHash nor the FxHash comparison —
// see ../README.md § Benchmarks.

package main

import "fmt"

func nthLetter(n int64) byte {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	return alphabet[n%26]
}

func replaceChar(word string, pos int64, newCh byte) string {
	out := make([]byte, 0, len(word))
	for i := 0; i < len(word); i++ {
		if int64(i) == pos {
			out = append(out, newCh)
		} else {
			out = append(out, word[i])
		}
	}
	return string(out)
}

func neighbors(word string, wordSet map[string]int64) []string {
	out := make([]string, 0)
	n := int64(len(word))
	for i := int64(0); i < n; i++ {
		orig := word[i]
		for c := int64(0); c < 26; c++ {
			if (c + 97) != int64(orig) {
				cand := replaceChar(word, i, nthLetter(c))
				if _, ok := wordSet[cand]; ok {
					out = append(out, cand)
				}
			}
		}
	}
	return out
}

func ladderLength(begin string, end string, words []string) int64 {
	wordSet := make(map[string]int64)
	for wi := 0; wi < len(words); wi++ {
		wordSet[words[wi]] = 1
	}
	if _, ok := wordSet[end]; !ok {
		return 0
	}

	visited := make(map[string]int64)
	visited[begin] = 1
	cur := []string{begin}
	steps := int64(1)

	for len(cur) > 0 {
		nxt := make([]string, 0)
		for i := 0; i < len(cur); i++ {
			word := cur[i]
			if word == end {
				return steps
			}
			nbs := neighbors(word, wordSet)
			for j := 0; j < len(nbs); j++ {
				nb := nbs[j]
				if _, ok := visited[nb]; !ok {
					visited[nb] = 1
					nxt = append(nxt, nb)
				}
			}
		}
		cur = nxt
		steps++
	}
	return 0
}

func main() {
	const alpha int64 = 5
	const wlen int64 = 5
	const iters int64 = 17
	const total int64 = 3125

	words := make([]string, 0, total)
	for idx := int64(0); idx < total; idx++ {
		w := make([]byte, 0, wlen)
		rem := idx
		div := int64(625)
		for d := int64(0); d < wlen; d++ {
			digit := rem / div
			w = append(w, nthLetter(digit))
			rem -= digit * div
			div /= alpha
		}
		words = append(words, string(w))
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		b := (it * 257) % total
		e := (it*613 + 1234) % total
		r := ladderLength(words[b], words[e], words)
		sink = (sink*31 + r) % 1000000007
	}
	fmt.Println(sink)
}
