// LeetCode #8 — Go goroutine-parallel mirror (par lane, atoi).
// Same one-pass myAtoi; the K=10M reduction is split across NumCPU
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

func myAtoi(s string) int32 {
	bytes := []byte(s)
	ln := len(bytes)

	const space byte = ' '
	const plus byte = '+'
	const minus byte = '-'
	const zero byte = '0'
	const nine byte = '9'

	i := 0
	for i < ln && bytes[i] == space {
		i++
	}

	sign := int32(1)
	if i < ln && bytes[i] == plus {
		i++
	} else if i < ln && bytes[i] == minus {
		sign = -1
		i++
	}

	const intMax int32 = 2147483647
	const intMin int32 = -2147483648
	const maxDiv int32 = intMax / 10

	var result int32
	for i < ln {
		b := bytes[i]
		if b < zero || b > nine {
			break
		}
		digit := int32(b - zero)
		if result > maxDiv || (result == maxDiv && digit > 7) {
			if sign == 1 {
				return intMax
			}
			return intMin
		}
		result = result*10 + digit
		i++
	}

	return sign * result
}

func main() {
	inputs := []string{
		"42",
		"   -42",
		"4193 with words",
		"91283472332",
		"+1",
		"  0000000000012345678",
		"-2147483648",
		"  -0012a42",
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
				s += int64(myAtoi(inputs[idx]))
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
