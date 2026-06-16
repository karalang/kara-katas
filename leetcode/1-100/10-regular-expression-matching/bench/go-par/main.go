// LeetCode #10 — Go goroutine-parallel mirror (par lane, regex).
// Same recursive isMatchAt; the K=10M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n      = 8
	kIters = 10_000_000
)

func isMatchAt(s string, i int, p string, j int) bool {
	nn := len(s)
	m := len(p)

	if j == m {
		return i == nn
	}

	firstMatch := i < nn && (p[j] == s[i] || p[j] == '.')

	if j+1 < m && p[j+1] == '*' {
		return isMatchAt(s, i, p, j+2) ||
			(firstMatch && isMatchAt(s, i+1, p, j))
	}

	return firstMatch && isMatchAt(s, i+1, p, j+1)
}

func isMatch(s string, p string) bool {
	return isMatchAt(s, 0, p, 0)
}

func main() {
	strs := []string{
		"aa",
		"ab",
		"aab",
		"mississippi",
		"aaaaaaaaaab",
		"aaa",
		"abc",
		"aaab",
	}
	pats := []string{
		"a*",
		".*",
		"c*a*b",
		"mis*is*p*.",
		"a*a*a*a*a*b",
		"ab*a",
		"...",
		"a*b",
	}

	workers := runtime.NumCPU()
	if workers > kIters {
		workers = kIters
	}
	chunk := int64(kIters / workers)
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for wk := 0; wk < workers; wk++ {
		go func(wk int) {
			defer wg.Done()
			start := int64(wk) * chunk
			end := start + chunk
			if wk == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				idx := k % n
				if isMatch(strs[idx], pats[idx]) {
					s += 1
				}
			}
			partials[wk] = s
		}(wk)
	}
	wg.Wait()
	var sum int64
	for _, p := range partials {
		sum += p
	}
	fmt.Println(sum)
}
