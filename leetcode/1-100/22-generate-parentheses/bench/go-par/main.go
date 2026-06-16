// LeetCode #22 — Go goroutine-parallel mirror (par lane, backtracking).
// Same owned-snapshot recursive backtracking; the K=150 iter reduction is
// split across NumCPU workers (per-worker partial + merge). Hand-tuned-
// parallel comparator. Sink matches the kara/rust/c/go mirrors (50,388,000).
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n     = 10
	iters = 150
)

func backtrack(cur string, open, close, nn int, out *[]string) {
	if close == nn {
		*out = append(*out, cur)
		return
	}
	if open < nn {
		backtrack(cur+"(", open+1, close, nn, out)
	}
	if close < open {
		backtrack(cur+")", open, close+1, nn, out)
	}
}

func generateParenthesis(nn int) []string {
	out := make([]string, 0)
	backtrack("", 0, 0, nn, &out)
	return out
}

func main() {
	workers := runtime.NumCPU()
	if workers > iters {
		workers = iters
	}
	chunk := iters / workers
	partials := make([]uint64, workers)
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
			var s uint64
			for k := start; k < end; k++ {
				combos := generateParenthesis(n)
				var bytes uint64
				for _, c := range combos {
					bytes += uint64(len(c))
				}
				s += bytes
			}
			partials[w] = s
		}(w)
	}
	wg.Wait()
	var total uint64
	for _, p := range partials {
		total += p
	}
	fmt.Println(total) // 150 * 16796 * 20 = 50,388,000
}
