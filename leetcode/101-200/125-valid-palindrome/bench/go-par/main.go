// LeetCode #125 — Go goroutine-parallel mirror (par lane).
//
// Same allocating filter-then-compare as ../go-seq/main.go, but the ITERS
// reduction is split across runtime.NumCPU() workers — each sums a private
// chunk into a per-worker partial, then a final merge. Hand-tuned-parallel
// comparator for Kāra's auto-par: the programmer writes the chunking +
// sync.WaitGroup + partial-merge boilerplate by hand. Same sink (3000000).
package main

import (
	"fmt"
	"runtime"
	"strings"
	"sync"
)

const iters = 3000000

func isAlnum(b byte) bool {
	return (b >= '0' && b <= '9') || (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z')
}

func isPalindrome(s []byte) bool {
	clean := make([]byte, 0, len(s))
	for _, b := range s {
		if isAlnum(b) {
			if b >= 'A' && b <= 'Z' {
				b += 32
			}
			clean = append(clean, b)
		}
	}
	lo, hi := 0, len(clean)-1
	for lo < hi {
		if clean[lo] != clean[hi] {
			return false
		}
		lo++
		hi--
	}
	return true
}

func main() {
	input := []byte(strings.Repeat("A man, a plan, a canal: Panama", 8))
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
				if isPalindrome(input) {
					s++
				}
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
