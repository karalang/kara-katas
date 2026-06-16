// LeetCode #65 — Go goroutine-parallel mirror (par lane, valid).
// Same 8-state DFA is_number; the K=10M reduction is split across NumCPU
// workers (per-worker partial + merge). Hand-tuned-parallel comparator.
// Sink matches the kara/rust/c/go mirrors.
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

func categorize(b byte) int32 {
	if b >= '0' && b <= '9' {
		return 0
	}
	if b == '+' || b == '-' {
		return 1
	}
	if b == '.' {
		return 2
	}
	if b == 'e' || b == 'E' {
		return 3
	}
	return 4
}

func isNumber(s string) bool {
	bytes := []byte(s)
	ln := len(bytes)

	state := int32(0)
	for i := 0; i < ln; i++ {
		cat := categorize(bytes[i])

		switch state {
		case 0:
			switch cat {
			case 0:
				state = 2
			case 1:
				state = 1
			case 2:
				state = 3
			default:
				return false
			}
		case 1:
			switch cat {
			case 0:
				state = 2
			case 2:
				state = 3
			default:
				return false
			}
		case 2:
			switch cat {
			case 0:
				state = 2
			case 2:
				state = 4
			case 3:
				state = 6
			default:
				return false
			}
		case 3:
			switch cat {
			case 0:
				state = 5
			default:
				return false
			}
		case 4:
			switch cat {
			case 0:
				state = 5
			case 3:
				state = 6
			default:
				return false
			}
		case 5:
			switch cat {
			case 0:
				state = 5
			case 3:
				state = 6
			default:
				return false
			}
		case 6:
			switch cat {
			case 0:
				state = 8
			case 1:
				state = 7
			default:
				return false
			}
		case 7:
			switch cat {
			case 0:
				state = 8
			default:
				return false
			}
		case 8:
			switch cat {
			case 0:
				state = 8
			default:
				return false
			}
		default:
			return false
		}
	}

	return state == 2 || state == 4 || state == 5 || state == 8
}

func main() {
	inputs := []string{
		"0",
		"-.9",
		"53.5e93",
		"+6e-1",
		"abc",
		"1e",
		"99e2.5",
		"-123.456e789",
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
				if isNumber(inputs[idx]) {
					s++
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
