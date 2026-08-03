// Benchmark mirror for LeetCode #245 - Shortest Word Distance III.
//
// Same algorithm, same LCG, same sink as the Kara/C/Rust/Python mirrors, and
// the same workload as #243's bench so the two are directly comparable. Half
// the punches are same-word queries - the case #243 cannot answer.
//
// strings.Clone per slot is load-bearing, same as in #243: Go's string == has a
// pointer-equality fast path, and letting list[i] alias its vocabulary entry
// would hand this lane a free win the other four do not get.
package main

import (
	"fmt"
	"strings"
)

const (
	vocabN = 256
	n      = 20000
	iters  = 2000
)

func shortestWordDistance(words []string, word1, word2 string) int64 {
	total := int64(len(words))
	same := word1 == word2
	best := total
	prev := int64(-1)
	for i := int64(0); i < total; i++ {
		w := words[i]
		if w == word1 || w == word2 {
			if prev >= 0 && (same || words[prev] != w) {
				if i-prev < best {
					best = i - prev
				}
			}
			prev = i
		}
	}
	return best
}

func lcg(state int64) int64 {
	return (state*1103515245 + 12345) & 2147483647
}

func main() {
	alpha := []string{"a", "b", "c", "d"}

	vocab := make([]string, 0, vocabN)
	for v := 0; v < vocabN; v++ {
		vocab = append(vocab, "delta"+alpha[(v/64)%4]+alpha[(v/16)%4]+alpha[(v/4)%4]+alpha[v%4])
	}

	list := make([]string, 0, n)
	state := int64(1)
	for i := 0; i < n; i++ {
		state = lcg(state)
		list = append(list, strings.Clone(vocab[(state/65536)%vocabN]))
	}

	var acc int64
	qstate := int64(7)
	for k := 0; k < iters; k++ {
		qstate = lcg(qstate)
		a := (qstate / 65536) % vocabN
		qstate = lcg(qstate)
		b := (qstate / 65536) % vocabN
		if b == a {
			b = (b + 1) % vocabN
		}
		var d int64
		if k%2 == 0 {
			d = shortestWordDistance(list, vocab[a], vocab[a])
		} else {
			d = shortestWordDistance(list, vocab[a], vocab[b])
		}
		acc = (acc*131 + d) % 1000000007
	}
	fmt.Println(acc)
}
