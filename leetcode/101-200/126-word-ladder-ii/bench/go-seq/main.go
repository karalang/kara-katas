// Benchmark harness for LeetCode #126 — Word Ladder II.
// Mirrors word_ladder_ii.kara algorithm-for-algorithm.
//
// Go's map[string]T hashes with an AES-NI-based function it does not let you
// swap, so this lane sits on a third hash — neither SipHash nor FxHash. See
// ../README.md § Benchmarks.

package main

import "fmt"

const MOD int64 = 1000000007

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
			ch := nthLetter(c)
			if (c + 97) != int64(orig) {
				cand := replaceChar(word, i, ch)
				if _, ok := wordSet[cand]; ok {
					out = append(out, cand)
				}
			}
		}
	}
	return out
}

func pathDigest(path []string) int64 {
	var h int64 = 0
	for idx := len(path) - 1; idx >= 0; idx-- {
		w := path[idx]
		for i := 0; i < len(w); i++ {
			h = (h*131 + (int64(w[i]) - 96)) % MOD
		}
		h = (h*131 + 27) % MOD
	}
	return h
}

func dfs(word string, begin string, preds map[string][]string, path *[]string,
	count *int64, digest *int64) {
	if word == begin {
		*digest = (*digest + pathDigest(*path)) % MOD
		*count++
		return
	}
	plist, ok := preds[word]
	if !ok {
		return
	}
	for i := 0; i < len(plist); i++ {
		p := plist[i]
		*path = append(*path, p)
		dfs(p, begin, preds, path, count, digest)
		*path = (*path)[:len(*path)-1]
	}
}

type ladderResult struct {
	count  int64
	length int64
	digest int64
}

func findLadders(begin string, end string, words []string) ladderResult {
	wordSet := make(map[string]int64)
	for wi := 0; wi < len(words); wi++ {
		wordSet[words[wi]] = 1
	}
	if _, ok := wordSet[end]; !ok {
		return ladderResult{0, 0, 0}
	}

	preds := make(map[string][]string)
	visited := make(map[string]int64)
	visited[begin] = 1
	cur := []string{begin}
	found := false
	depth := int64(1)

	for len(cur) > 0 && !found {
		inNext := make(map[string]int64)
		nxt := make([]string, 0)
		for i := 0; i < len(cur); i++ {
			word := cur[i]
			nbs := neighbors(word, wordSet)
			for j := 0; j < len(nbs); j++ {
				nb := nbs[j]
				if _, ok := visited[nb]; !ok {
					plist, has := preds[nb]
					if !has {
						plist = make([]string, 0)
					} else {
						cp := make([]string, len(plist))
						copy(cp, plist)
						plist = cp
					}
					plist = append(plist, word)
					preds[nb] = plist
					if _, ok := inNext[nb]; !ok {
						if nb == end {
							found = true
						}
						inNext[nb] = 1
						nxt = append(nxt, nb)
					}
				}
			}
		}
		for k := 0; k < len(nxt); k++ {
			visited[nxt[k]] = 1
		}
		cur = nxt
		depth++
	}

	if !found {
		return ladderResult{0, 0, 0}
	}

	path := []string{end}
	var count int64 = 0
	var digest int64 = 0
	dfs(end, begin, preds, &path, &count, &digest)

	return ladderResult{count, depth, digest}
}

func main() {
	const alpha int64 = 5
	const wlen int64 = 5
	const iters int64 = 24
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
		r := findLadders(words[b], words[e], words)
		sink = (sink*1000003 + r.count*7 + r.length*13 + r.digest) % MOD
	}
	fmt.Println(sink)
}
