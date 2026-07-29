// Benchmark harness for LeetCode #243 — Shortest Word Distance.
// Mirrors shortest_distance.kara algorithm-for-algorithm.
//
// strings.Clone per slot is load-bearing, not decoration. A Go string is an
// immutable (pointer, len) view, so `list[i] = vocab[j]` would make every slot
// holding word j share one data pointer — and Go's string `==` short-circuits
// true on pointer equality. That would hand this lane a free win on exactly the
// comparisons that matter, which the other four mirrors don't get. Cloning gives
// each slot its own buffer so every lane pays length-check-then-memcmp.
package main

import (
	"fmt"
	"strings"
)

const (
	VocabN = 256
	N      = 20000
	Iters  = 2000
)

func shortestDistance(words []string, word1, word2 string) int64 {
	n := int64(len(words))
	last1, last2 := int64(-1), int64(-1)
	best := n
	for i := int64(0); i < n; i++ {
		if words[i] == word1 {
			last1 = i
			if last2 >= 0 && last1-last2 < best {
				best = last1 - last2
			}
		} else if words[i] == word2 {
			last2 = i
			if last1 >= 0 && last2-last1 < best {
				best = last2 - last1
			}
		}
	}
	return best
}

// Overflow-free 31-bit LCG; every draw uses bits 16..23.
func lcg(state int64) int64 {
	return (state*1103515245 + 12345) & 2147483647
}

func main() {
	alpha := []string{"a", "b", "c", "d"}

	vocab := make([]string, 0, VocabN)
	for v := int64(0); v < VocabN; v++ {
		var w strings.Builder
		w.WriteString("delta")
		w.WriteString(alpha[(v/64)%4])
		w.WriteString(alpha[(v/16)%4])
		w.WriteString(alpha[(v/4)%4])
		w.WriteString(alpha[v%4])
		vocab = append(vocab, w.String())
	}

	list := make([]string, 0, N)
	state := int64(1)
	for i := int64(0); i < N; i++ {
		state = lcg(state)
		list = append(list, strings.Clone(vocab[(state/65536)%VocabN]))
	}

	var acc int64
	qstate := int64(7)
	for k := int64(0); k < Iters; k++ {
		qstate = lcg(qstate)
		a := (qstate / 65536) % VocabN
		qstate = lcg(qstate)
		b := (qstate / 65536) % VocabN
		if b == a {
			b = (b + 1) % VocabN
		}
		d := shortestDistance(list, vocab[a], vocab[b])
		acc = (acc*131 + d) % 1000000007
	}
	fmt.Println(acc)
}
