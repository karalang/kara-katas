// LeetCode #13 — Go goroutine-parallel mirror (par lane, greedy).
// Same int_to_roman / roman_to_int; the K=10M reduction is split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const kIters = 10_000_000

func intToRoman(num int64) []int32 {
	out := make([]int32, 0, 15)
	n := num
	for n >= 1000 {
		out = append(out, 'M')
		n -= 1000
	}
	if n >= 900 {
		out = append(out, 'C', 'M')
		n -= 900
	}
	if n >= 500 {
		out = append(out, 'D')
		n -= 500
	}
	if n >= 400 {
		out = append(out, 'C', 'D')
		n -= 400
	}
	for n >= 100 {
		out = append(out, 'C')
		n -= 100
	}
	if n >= 90 {
		out = append(out, 'X', 'C')
		n -= 90
	}
	if n >= 50 {
		out = append(out, 'L')
		n -= 50
	}
	if n >= 40 {
		out = append(out, 'X', 'L')
		n -= 40
	}
	for n >= 10 {
		out = append(out, 'X')
		n -= 10
	}
	if n >= 9 {
		out = append(out, 'I', 'X')
		n -= 9
	}
	if n >= 5 {
		out = append(out, 'V')
		n -= 5
	}
	if n >= 4 {
		out = append(out, 'I', 'V')
		n -= 4
	}
	for n >= 1 {
		out = append(out, 'I')
		n -= 1
	}
	return out
}

func value(c int32) int64 {
	switch c {
	case 'I':
		return 1
	case 'V':
		return 5
	case 'X':
		return 10
	case 'L':
		return 50
	case 'C':
		return 100
	case 'D':
		return 500
	case 'M':
		return 1000
	}
	return 0
}

func romanToInt(r []int32) int64 {
	n := len(r)
	var total int64 = 0
	for i := 0; i < n; i++ {
		cur := value(r[i])
		if i+1 < n {
			nxt := value(r[i+1])
			if cur < nxt {
				total -= cur
			} else {
				total += cur
			}
		} else {
			total += cur
		}
	}
	return total
}

func main() {
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
				raw := k*2654435769 + 305419896
				num := (raw%3999+3999)%3999 + 1
				r := intToRoman(num)
				s += romanToInt(r)
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
