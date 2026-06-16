// LeetCode #6 — Go goroutine-parallel mirror (par lane, row_buffers).
// Same row-buffer convertOff; the K=10K reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n       = 10000
	rPeriod = 1000
	kIters  = 10000
	numRows = 4
)

func convertOff(chars []rune, off, length, numRows int) []rune {
	if numRows <= 1 || numRows >= length {
		out := make([]rune, length)
		copy(out, chars[off:off+length])
		return out
	}

	rows := make([][]rune, numRows)
	cur := 0
	goingDown := false
	for i := 0; i < length; i++ {
		rows[cur] = append(rows[cur], chars[off+i])
		if cur == 0 || cur == numRows-1 {
			goingDown = !goingDown
		}
		if goingDown {
			cur++
		} else {
			cur--
		}
	}

	var out []rune
	for _, row := range rows {
		out = append(out, row...)
	}
	return out
}

func main() {
	pattern := []rune("PAYPALISHIRING")
	need := n + rPeriod
	var chars []rune
	for len(chars) < need {
		chars = append(chars, pattern...)
	}

	workers := runtime.NumCPU()
	if workers > kIters {
		workers = kIters
	}
	chunk := kIters / workers
	partials := make([]int64, workers)
	var wg sync.WaitGroup
	wg.Add(workers)
	for wk := 0; wk < workers; wk++ {
		go func(wk int) {
			defer wg.Done()
			start := wk * chunk
			end := start + chunk
			if wk == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				off := k % rPeriod
				result := convertOff(chars, off, n, numRows)
				last := len(result) - 1
				s += int64(result[0]) + int64(result[last])
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
