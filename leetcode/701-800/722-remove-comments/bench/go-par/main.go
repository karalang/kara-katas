// LeetCode #722 — Go goroutine-parallel mirror (par lane).
//
// Same byte-indexed segment-slicing removeComments as ../go-seq/main.go, but the
// ITERS reduction is split across runtime.NumCPU() workers (per-worker partial
// sum, final merge). Hand-tuned-parallel comparator for Kāra's auto-par: the
// programmer writes the chunking + sync.WaitGroup + partial-merge boilerplate by
// hand; Kāra parallelizes the identical reduction with no source change. Same
// sink (30960000) as every other mirror.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	reps  = 60
	iters = 4000
)

var template = []string{
	"int main() {            // entry point",
	"  int a = 1; /* inline */ int b = 2;",
	"  /* a multi-line",
	"     block comment that",
	"     spans several lines */ int c = a + b;",
	"  // a full line comment",
	"  int e = c * 3;        /* trailing block */",
	"  int d = a /* x */ + b /* y */ + c;",
	"  return d * 2;//done",
	"}",
}

func removeComments(source []string) []string {
	result := make([]string, 0, len(source))
	buffer := make([]byte, 0, 64)
	inBlock := false
	for _, line := range source {
		n := len(line)
		segStart := 0
		i := 0
		for i < n {
			if !inBlock {
				if i+1 < n && line[i] == '/' && line[i+1] == '/' {
					buffer = append(buffer, line[segStart:i]...)
					segStart = n
					break
				} else if i+1 < n && line[i] == '/' && line[i+1] == '*' {
					buffer = append(buffer, line[segStart:i]...)
					inBlock = true
					i += 2
				} else {
					i++
				}
			} else {
				if i+1 < n && line[i] == '*' && line[i+1] == '/' {
					inBlock = false
					i += 2
					segStart = i
				} else {
					i++
				}
			}
		}
		if !inBlock {
			buffer = append(buffer, line[segStart:n]...)
			if len(buffer) > 0 {
				result = append(result, string(buffer))
				buffer = buffer[:0]
			}
		}
	}
	return result
}

func passLen(source []string) int64 {
	var total int64
	for _, s := range removeComments(source) {
		total += int64(len(s))
	}
	return total
}

func main() {
	lines := make([]string, 0, reps*len(template))
	for r := 0; r < reps; r++ {
		lines = append(lines, template...)
	}

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
				s += passLen(lines)
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
