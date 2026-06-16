// LeetCode #20 — Go goroutine-parallel mirror (par lane, valid_parentheses).
// Same byte-buffer build + stack-of-expected-closers validate; the K=500k
// count-reduction is split across NumCPU workers (per-worker partial +
// merge). Hand-tuned-parallel comparator. Sink matches the kara/rust/c/go
// mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	depth  = 1000
	kIters = 500_000
)

func isValidBytes(bytes []byte) bool {
	stack := make([]byte, 0)
	for _, b := range bytes {
		if b == '(' || b == '[' || b == '{' {
			var closer byte
			if b == '(' {
				closer = ')'
			} else if b == '[' {
				closer = ']'
			} else {
				closer = '}'
			}
			stack = append(stack, closer)
		} else {
			if len(stack) == 0 {
				return false
			}
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			if top != b {
				return false
			}
		}
	}
	return len(stack) == 0
}

func buildBrackets(depth int64, kind int64, corrupt bool) []byte {
	var op, cl, wrong byte = '(', ')', ']'
	if kind == 1 {
		op, cl, wrong = '[', ']', ')'
	} else if kind == 2 {
		op, cl, wrong = '{', '}', ')'
	}
	buf := make([]byte, 0)
	for i := int64(0); i < depth; i++ {
		buf = append(buf, op)
	}
	for i := int64(0); i < depth-1; i++ {
		buf = append(buf, cl)
	}
	if corrupt {
		buf = append(buf, wrong)
	} else {
		buf = append(buf, cl)
	}
	return buf
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
				kind := k % 3
				corrupt := (k % 7) == 0
				buf := buildBrackets(depth, kind, corrupt)
				if isValidBytes(buf) {
					s++
				}
			}
			partials[wk] = s
		}(wk)
	}
	wg.Wait()
	var count int64
	for _, p := range partials {
		count += p
	}
	fmt.Println(count)
}
