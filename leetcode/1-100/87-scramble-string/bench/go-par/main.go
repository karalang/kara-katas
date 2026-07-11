// LeetCode #87 — goroutine-parallel Go mirror (par lane).
// Same batch of K=60000 independent memoized scramble decisions as ../go-seq/main.go;
// the associative sum reduction is split across GOMAXPROCS goroutines (chunked seed
// range, WaitGroup join, merge). Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the seq mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func scramble(s1 []byte, i1 int64, s2 []byte, i2, length int64, memo []int64, n int64) bool {
	if length == 0 {
		return true
	}
	key := (i1*n + i2) * (n + 1) + length
	if memo[key] != -1 {
		return memo[key] == 1
	}
	equal := true
	for k := int64(0); k < length; k++ {
		if s1[i1+k] != s2[i2+k] {
			equal = false
			break
		}
	}
	if equal {
		memo[key] = 1
		return true
	}
	var counts [26]int64
	for k := int64(0); k < length; k++ {
		counts[s1[i1+k]-97]++
		counts[s2[i2+k]-97]--
	}
	for c := 0; c < 26; c++ {
		if counts[c] != 0 {
			memo[key] = 0
			return false
		}
	}
	for split := int64(1); split < length; split++ {
		if scramble(s1, i1, s2, i2, split, memo, n) &&
			scramble(s1, i1+split, s2, i2+split, length-split, memo, n) {
			memo[key] = 1
			return true
		}
		if scramble(s1, i1, s2, i2+length-split, split, memo, n) &&
			scramble(s1, i1+split, s2, i2, length-split, memo, n) {
			memo[key] = 1
			return true
		}
	}
	memo[key] = 0
	return false
}

func one(length, seed int64) int64 {
	s1 := make([]byte, length)
	for j := int64(0); j < length; j++ {
		s1[j] = byte(97 + (j % 8))
	}
	s2 := make([]byte, length)
	for j := int64(0); j < length; j++ {
		s2[j] = s1[(j*5+seed)%length]
	}
	cells := length * length * (length + 1)
	memo := make([]int64, cells)
	for i := int64(0); i < cells; i++ {
		memo[i] = -1
	}
	var r int64 = 0
	if scramble(s1, 0, s2, 0, length, memo, length) {
		r = 1
	}
	h := r
	for i := int64(0); i < cells; i++ {
		h = (h*131 + (memo[i] + 2)) % 1000000007
	}
	return h
}

func main() {
	const length = 12
	const total int64 = 60000
	nw := int64(runtime.GOMAXPROCS(0))
	if nw < 1 {
		nw = 1
	}
	if nw > total {
		nw = total
	}
	partials := make([]int64, nw)
	chunk := total / nw
	var wg sync.WaitGroup
	for w := int64(0); w < nw; w++ {
		start := w * chunk
		end := (w + 1) * chunk
		if w == nw-1 {
			end = total
		}
		wg.Add(1)
		go func(idx, s, e int64) {
			defer wg.Done()
			var acc int64 = 0
			for i := s; i < e; i++ {
				acc += one(length, i)
			}
			partials[idx] = acc
		}(w, start, end)
	}
	wg.Wait()
	var totalSum int64 = 0
	for w := int64(0); w < nw; w++ {
		totalSum += partials[w]
	}
	fmt.Println(totalSum)
}
