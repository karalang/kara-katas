// LeetCode #17 — Go goroutine-parallel mirror (par lane, letter_combinations).
// Same BFS letter_combinations; the K=100k reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	mCases = 8
	kIters = 100_000
)

func letterCombinations(digits string) []string {
	out := make([]string, 0)
	if len(digits) == 0 {
		return out
	}
	groups := [8]string{"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}

	out = append(out, "")
	for d := 0; d < len(digits); d++ {
		idx := int(digits[d] - '2')
		letters := groups[idx]
		prevLen := len(out)
		next := make([]string, 0)
		for i := 0; i < prevLen; i++ {
			for _, letter := range letters {
				next = append(next, out[i]+string(letter))
			}
		}
		out = next
	}
	return out
}

func main() {
	cases := [8]string{"", "2", "7", "23", "79", "234", "279", "2349"}

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
				idx := k % mCases
				s += int64(len(letterCombinations(cases[idx])))
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
