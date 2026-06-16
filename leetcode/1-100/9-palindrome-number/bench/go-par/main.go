// LeetCode #9 — Go goroutine-parallel mirror (par lane, palindrome).
// Same half-reverse isPalindrome; the K=50M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n      = 1024
	kIters = 50_000_000
)

func isPalindrome(x int32) bool {
	if x < 0 || (x%10 == 0 && x != 0) {
		return false
	}
	var reversed int32 = 0
	for x > reversed {
		reversed = reversed*10 + x%10
		x /= 10
	}
	return x == reversed || x == reversed/10
}

func manufacturePalindrome(v32 int32) int32 {
	var lo int32
	if v32 < 0 {
		lo = -v32
	} else {
		lo = v32
	}
	fourRaw := lo % 10000
	var four int32
	if fourRaw < 1000 {
		four = fourRaw + 1000
	} else {
		four = fourRaw
	}
	d0 := four % 10
	d1 := (four / 10) % 10
	d2 := (four / 100) % 10
	d3 := (four / 1000) % 10
	rev := d0*1000 + d1*100 + d2*10 + d3
	return four*10000 + rev
}

func main() {
	inputs := make([]int32, n)
	for i := int64(0); i < n; i++ {
		raw := i*2654435769 + 305419896
		v32 := int32(raw)
		if i%16 == 0 {
			inputs[i] = manufacturePalindrome(v32)
		} else {
			inputs[i] = v32
		}
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
				if isPalindrome(inputs[idx]) {
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
