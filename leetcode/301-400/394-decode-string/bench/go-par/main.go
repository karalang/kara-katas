// LeetCode #394 — Go goroutine-parallel mirror (par lane).
//
// Same iterative-stack decode as ../go-seq/main.go, but the ITERS reduction is
// split across runtime.NumCPU() workers — each sums a private chunk into a
// per-worker partial, then a final merge. The hand-tuned-parallel comparator
// for Kāra's auto-par: the programmer writes the chunking + sync.WaitGroup +
// partial-merge boilerplate by hand; Kāra parallelizes the identical reduction
// with no source change. Same sink (41600000) as every other mirror.
package main

import (
	"fmt"
	"runtime"
	"strings"
	"sync"
)

const (
	encoded = "3[ab2[cd]ef]5[gh]2[ij3[kl]m]"
	iters   = 800000
)

func isLetter(b byte) bool {
	return b != '[' && b != ']' && !(b >= '0' && b <= '9')
}

func decodeString(s string) string {
	var strStack []string
	var numStack []int64
	cur := ""
	var k int64 = 0
	n := len(s)
	i := 0
	for i < n {
		b := s[i]
		if b >= '0' && b <= '9' {
			k = k*10 + int64(b-'0')
			i++
		} else if b == '[' {
			strStack = append(strStack, cur)
			numStack = append(numStack, k)
			cur = ""
			k = 0
			i++
		} else if b == ']' {
			count := numStack[len(numStack)-1]
			numStack = numStack[:len(numStack)-1]
			prev := strStack[len(strStack)-1]
			strStack = strStack[:len(strStack)-1]
			cur = prev + strings.Repeat(cur, int(count))
			i++
		} else {
			j := i
			for j < n && isLetter(s[j]) {
				j++
			}
			cur += s[i:j]
			i = j
		}
	}
	return cur
}

func main() {
	workers := runtime.NumCPU()
	chunk := iters / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)

	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := w * chunk
			end := start + chunk
			if w == workers-1 {
				end = iters
			}
			var s int64
			for it := start; it < end; it++ {
				s += int64(len(decodeString(encoded)))
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()

	var total int64
	for _, p := range partials {
		total += p
	}
	fmt.Println(total)
}
