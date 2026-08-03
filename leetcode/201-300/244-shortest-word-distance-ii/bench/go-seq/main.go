// Benchmark mirror for LeetCode #244 - Shortest Word Distance II.
//
// Same algorithm, same LCG, same sink as the Kara/C/Rust/Python mirrors: build
// the 20,000-word list and its position index ONCE (index-pool construction -
// word -> slot in a map, plus a side [][]int64), then punch 200,000
// two-pointer merge queries.
//
// strings.Clone per slot is load-bearing, same as in #243: Go's string
// comparison and map hashing can short-circuit on operands that share a data
// pointer, and letting list[i] alias its vocabulary entry would hand this lane
// a free win the other four do not get.
package main

import (
	"fmt"
	"strings"
)

const (
	vocabN = 256
	n      = 20000
	iters  = 200000
)

type wordDistance struct {
	slot  map[string]int
	lists [][]int64
	size  int64
}

func newWordDistance(words []string) *wordDistance {
	wd := &wordDistance{
		slot:  make(map[string]int),
		lists: make([][]int64, 0),
		size:  int64(len(words)),
	}
	for i, w := range words {
		if s, ok := wd.slot[w]; ok {
			wd.lists[s] = append(wd.lists[s], int64(i))
		} else {
			wd.slot[w] = len(wd.lists)
			wd.lists = append(wd.lists, []int64{int64(i)})
		}
	}
	return wd
}

func (wd *wordDistance) shortest(word1, word2 string) int64 {
	s1, ok := wd.slot[word1]
	if !ok {
		return wd.size
	}
	s2, ok := wd.slot[word2]
	if !ok {
		return wd.size
	}
	p1 := wd.lists[s1]
	p2 := wd.lists[s2]
	best := wd.size
	a, b := 0, 0
	for a < len(p1) && b < len(p2) {
		d := p1[a] - p2[b]
		if d < 0 {
			d = -d
		}
		if d < best {
			best = d
		}
		if p1[a] < p2[b] {
			a++
		} else {
			b++
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
		w := "delta" + alpha[(v/64)%4] + alpha[(v/16)%4] + alpha[(v/4)%4] + alpha[v%4]
		vocab = append(vocab, w)
	}

	list := make([]string, 0, n)
	state := int64(1)
	for i := 0; i < n; i++ {
		state = lcg(state)
		list = append(list, strings.Clone(vocab[(state/65536)%vocabN]))
	}

	wd := newWordDistance(list)

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
		d := wd.shortest(vocab[a], vocab[b])
		acc = (acc*131 + d) % 1000000007
	}
	fmt.Println(acc)
}
