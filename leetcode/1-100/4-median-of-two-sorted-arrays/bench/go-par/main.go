// LeetCode #4 — Go goroutine-parallel mirror (par lane, binary_search_partition).
// Same middle_pair_off binary-search-partition; the K=10M reduction is split
// across NumCPU workers (per-worker partial + merge). Hand-tuned-parallel
// comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"math"
	"runtime"
	"sync"
)

const (
	M      = 1000000
	N      = 1000000
	R      = 1000
	kIters = 10_000_000
)

func middlePairOff(a []int64, aOff int64, aLen int64,
	b []int64, bOff int64, bLen int64) (int64, int64) {
	if aLen > bLen {
		return middlePairOff(b, bOff, bLen, a, aOff, aLen)
	}
	half := (aLen + bLen + 1) / 2
	var lo int64 = 0
	hi := aLen
	for lo <= hi {
		i := (lo + hi) / 2
		j := half - i
		var leftA, rightA, leftB, rightB int64
		if i > 0 {
			leftA = a[aOff+i-1]
		} else {
			leftA = math.MinInt64
		}
		if i < aLen {
			rightA = a[aOff+i]
		} else {
			rightA = math.MaxInt64
		}
		if j > 0 {
			leftB = b[bOff+j-1]
		} else {
			leftB = math.MinInt64
		}
		if j < bLen {
			rightB = b[bOff+j]
		} else {
			rightB = math.MaxInt64
		}
		if leftA > rightB {
			hi = i - 1
		} else if leftB > rightA {
			lo = i + 1
		} else {
			lower := leftA
			if leftB > lower {
				lower = leftB
			}
			if (aLen+bLen)%2 == 1 {
				return lower, lower
			}
			upper := rightA
			if rightB < upper {
				upper = rightB
			}
			return lower, upper
		}
	}
	panic("unreachable")
}

func main() {
	baseA := make([]int64, M+R)
	for p := int64(0); p < M+R; p++ {
		baseA[p] = 2 * p
	}
	baseB := make([]int64, N+R)
	for p := int64(0); p < N+R; p++ {
		baseB[p] = 2*p + 1
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
				off := k % R
				lower, upper := middlePairOff(baseA, off, M, baseB, off, N)
				s += lower + upper
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
