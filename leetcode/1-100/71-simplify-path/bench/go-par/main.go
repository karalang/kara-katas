// LeetCode #71 — Go goroutine-parallel mirror (par lane, simplify).
// Same one-pass simplify; the K=1M reduction is split across NumCPU workers
// (per-worker partial + merge). Hand-tuned-parallel comparator. Sink (sum of
// simplified-output lengths) matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n      = 8
	kIters = 1_000_000
)

func simplify(s string, out []byte) int64 {
	cs := []rune(s)
	sn := int64(len(cs))

	var starts [64]int64
	var ends [64]int64
	var top int64 = 0

	var i int64 = 0
	for i < sn {
		for i < sn && cs[i] == '/' {
			i++
		}
		if i >= sn {
			break
		}
		j := i
		for j < sn && cs[j] != '/' {
			j++
		}
		length := j - i

		isDot := length == 1 && cs[i] == '.'
		isDotDot := length == 2 && cs[i] == '.' && cs[i+1] == '.'

		if isDot {
			// skip
		} else if isDotDot {
			if top > 0 {
				top--
			}
		} else {
			starts[top] = i
			ends[top] = j
			top++
		}
		i = j
	}

	if top == 0 {
		out[0] = '/'
		return 1
	}

	var pos int64 = 0
	for k := int64(0); k < top; k++ {
		out[pos] = '/'
		pos++
		a := starts[k]
		b := ends[k]
		for p := a; p < b; p++ {
			out[pos] = byte(cs[p])
			pos++
		}
	}
	return pos
}

func main() {
	inputs := [8]string{
		"/home/",
		"/home/user/Documents/../Pictures",
		"/.../a/../b/c/../d/./",
		"/a/b/c/../..",
		"/a//b////c/d//././/..",
		"/abc_123",
		"/a/b/../c/../../d",
		"/...hidden",
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
			var out [64]byte
			start := int64(wk) * chunk
			end := start + chunk
			if wk == workers-1 {
				end = kIters
			}
			var s int64
			for k := start; k < end; k++ {
				idx := k % n
				s += simplify(inputs[idx], out[:])
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
