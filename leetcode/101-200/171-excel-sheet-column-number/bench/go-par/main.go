// LeetCode #171 — Go goroutine-parallel mirror (par lane).
//
// Same Horner-fold base-26 parse as ../go-seq/main.go, but the K_ITERS reduction
// is split across runtime.NumCPU() workers (per-worker partial sum over a
// contiguous k-range, final merge; the corpus is built once, shared read-only).
// Hand-tuned-parallel comparator for Kāra's auto-par: the programmer writes the
// chunking + sync.WaitGroup + partial-merge boilerplate by hand; Kāra
// parallelizes the identical reduction with no source change. Same sink.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	length = 50000
	kIters = 100000000
)

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func toTitle(num int64) string {
	var tmp [16]byte
	ln := 0
	for num > 0 {
		num--
		tmp[ln] = letters[num%26]
		ln++
		num /= 26
	}
	out := make([]byte, ln)
	for i := 0; i < ln; i++ {
		out[i] = tmp[ln-1-i]
	}
	return string(out)
}

func toNumber(title string) int64 {
	var n int64
	for i := 0; i < len(title); i++ {
		n = n*26 + int64(title[i]-'A') + 1
	}
	return n
}

func main() {
	corpus := make([]string, length)
	for i := int64(0); i < length; i++ {
		corpus[i] = toTitle(i + 1)
	}

	workers := runtime.NumCPU()
	chunk := kIters / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)

	for w := 0; w < workers; w++ {
		go func(w int) {
			defer wg.Done()
			start := int64(w * chunk)
			end := start + int64(chunk)
			if w == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				s += toNumber(corpus[k%length])
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()

	var sum int64
	for _, p := range partials {
		sum += p
	}
	fmt.Println(sum)
}
