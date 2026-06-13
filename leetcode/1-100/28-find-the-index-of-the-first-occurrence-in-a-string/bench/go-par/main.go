// LeetCode #28 — Go goroutine-parallel mirror (par lane, brute_force).
// Same brute-force sliding-window str_str; the K-call reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel comparator
// for Kāra's auto-par. Sink = 199998400 (K=100 × first-match index 1999984).
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n     = 2000000
	m     = 16
	iters = 100
)

func strStr(haystack, needle []byte) int64 {
	hn := int64(len(haystack))
	nn := int64(len(needle))
	if nn == 0 {
		return 0
	}
	if nn > hn {
		return -1
	}
	for i := int64(0); i <= hn-nn; i++ {
		j := int64(0)
		for j < nn && haystack[i+j] == needle[j] {
			j++
		}
		if j == nn {
			return i
		}
	}
	return -1
}

func main() {
	haystack := make([]byte, n)
	for i := 0; i < n; i++ {
		haystack[i] = 'a'
	}
	haystack[n-1] = 'b'
	needle := make([]byte, m)
	for i := 0; i < m; i++ {
		needle[i] = 'a'
	}
	needle[m-1] = 'b'

	workers := runtime.NumCPU()
	if workers > iters {
		workers = iters
	}
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
			for k := start; k < end; k++ {
				s += strStr(haystack, needle)
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
