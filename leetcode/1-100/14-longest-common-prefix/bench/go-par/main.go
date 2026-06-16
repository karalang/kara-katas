// LeetCode #14 — Go goroutine-parallel mirror (par lane, vertical LCP).
// Same vertical-scan longestCommonPrefix; the K=1M reduction is split
// across NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	mCases   = 8
	nStrings = 16
	kIters   = 1_000_000
)

func nthLetter(n int64) byte {
	const alphabet = "abcdefghijklmnopqrstuvwxyz"
	return alphabet[n%26]
}

func makeString(prefixLen int64, suffixID int64) string {
	const alphabet = "abcdefghijklmnopqrstuvwxyz"
	out := make([]byte, 0, prefixLen+6)
	for i := int64(0); i < prefixLen; i++ {
		out = append(out, alphabet[i])
	}
	sig := nthLetter(suffixID)
	for j := 0; j < 6; j++ {
		out = append(out, sig)
	}
	return string(out)
}

func buildCase(prefixLen int64, count int64) []string {
	v := make([]string, 0, count)
	for s := int64(0); s < count; s++ {
		v = append(v, makeString(prefixLen, s))
	}
	return v
}

func prefixString(s string, k int64) string {
	out := make([]byte, 0, k)
	var i int64 = 0
	for _, c := range []byte(s) {
		if i >= k {
			break
		}
		out = append(out, c)
		i++
	}
	return string(out)
}

func longestCommonPrefix(strs []string) string {
	n := int64(len(strs))
	if n == 0 {
		return ""
	}
	first := []byte(strs[0])
	firstLen := int64(len(first))
	var col int64 = 0
	for col < firstLen {
		c := first[col]
		var s int64 = 1
		for s < n {
			other := []byte(strs[s])
			if col >= int64(len(other)) || other[col] != c {
				return prefixString(strs[0], col)
			}
			s++
		}
		col++
	}
	return prefixString(strs[0], firstLen)
}

func main() {
	prefixes := [8]int64{0, 2, 4, 7, 10, 13, 16, 20}

	sets := make([][]string, mCases)
	for m := int64(0); m < mCases; m++ {
		sets[m] = buildCase(prefixes[m], nStrings)
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
				idx := k % mCases
				s += int64(len(longestCommonPrefix(sets[idx])))
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
