// LeetCode #5 — Go goroutine-parallel mirror (par lane, expand_around_center).
// Same O(n²) expand-around-center longest_palindrome; the K=100-call reduction
// split across NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator for Kāra's auto-par. Sink = 500000 (K=100 × (0 + 5000)).
package main

import (
	"fmt"
	"runtime"
	"strings"
	"sync"
)

const (
	n     = 5000
	iters = 100
)

func expand(chars []rune, lo0, hi0 int64) (int64, int64) {
	lo, hi := lo0, hi0
	nn := int64(len(chars))
	for lo >= 0 && hi < nn && chars[lo] == chars[hi] {
		lo--
		hi++
	}
	return lo + 1, hi - lo - 1
}

func longestPalindrome(s string) (int64, int64) {
	chars := []rune(s)
	nn := int64(len(chars))
	var bestStart, bestLen int64
	for i := int64(0); i < nn; i++ {
		start, length := expand(chars, i, i)
		if length > bestLen {
			bestStart, bestLen = start, length
		}
		start, length = expand(chars, i, i+1)
		if length > bestLen {
			bestStart, bestLen = start, length
		}
	}
	return bestStart, bestLen
}

func main() {
	data := strings.Repeat("a", n)

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
				bs, bl := longestPalindrome(data)
				s += bs + bl
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
