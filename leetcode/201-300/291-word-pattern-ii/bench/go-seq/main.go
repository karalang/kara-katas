// Benchmark harness for LeetCode #291 — Word Pattern II backtracking.
// Mirrors word_pattern_ii.kara algorithm-for-algorithm.
package main

import "fmt"

func matches(p string, pi int, s string, si int, m map[string]string, used map[string]bool) bool {
	if pi >= len(p) {
		return si >= len(s)
	}
	if si >= len(s) {
		return false
	}

	key := p[pi : pi+1]
	if bound, ok := m[key]; ok {
		blen := len(bound)
		if si+blen > len(s) {
			return false
		}
		if s[si:si+blen] != bound {
			return false
		}
		return matches(p, pi+1, s, si+blen, m, used)
	}

	for end := si + 1; end <= len(s); end++ {
		cand := s[si:end]
		if !used[cand] {
			m[key] = cand
			used[cand] = true
			if matches(p, pi+1, s, end, m, used) {
				return true
			}
			delete(m, key)
			delete(used, cand)
		}
	}
	return false
}

func wordPatternMatch(p string, s string) bool {
	m := make(map[string]string)
	used := make(map[string]bool)
	return matches(p, 0, s, 0, m, used)
}

const (
	NP    = 8
	SL    = 30
	Iters = 500
)

func main() {
	alpha := []string{"a", "b", "c", "d"}
	subjects := make([]string, 0, NP)
	for j := 0; j < NP; j++ {
		sj := make([]byte, 0, SL)
		for k := 0; k < SL; k++ {
			kk := k
			if j%2 == 0 {
				kk = k % (SL / 2)
			}
			sj = append(sj, alpha[(kk*7+j*3)%4][0])
		}
		subjects = append(subjects, string(sj))
	}

	pat := "abcabc"
	var sink int64
	for it := 0; it < Iters; it++ {
		idx := (it * 5) % NP
		if wordPatternMatch(pat, subjects[idx]) {
			sink += int64(it) + 1
		} else {
			sink++
		}
	}
	fmt.Println(sink)
}
