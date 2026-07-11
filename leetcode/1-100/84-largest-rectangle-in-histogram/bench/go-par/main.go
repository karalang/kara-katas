// LeetCode #84 — goroutine-parallel Go mirror (par lane).
// Same batch of K=108000 independent largest-rectangle computations as
// ../go-seq/main.go; the associative sum reduction is split across GOMAXPROCS
// goroutines (chunked seed range, WaitGroup join, merge). Hand-tuned-parallel
// comparator for Kāra's auto-par. Sink matches the seq mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const n int64 = 2000

func largestRectangle(heights []int64, n int64) int64 {
	stack := make([]int64, 0, n+1)
	var maxArea int64 = 0
	for i := int64(0); i <= n; i++ {
		var h int64 = 0
		if i < n {
			h = heights[i]
		}
		for len(stack) > 0 && heights[stack[len(stack)-1]] > h {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			height := heights[top]
			var width int64
			if len(stack) == 0 {
				width = i
			} else {
				width = i - stack[len(stack)-1] - 1
			}
			area := height * width
			if area > maxArea {
				maxArea = area
			}
		}
		stack = append(stack, i)
	}
	return maxArea
}

func compute(seed int64) int64 {
	h := make([]int64, n)
	for j := int64(0); j < n; j++ {
		h[j] = (j + seed) % 50
	}
	return largestRectangle(h, n)
}

func main() {
	const total int64 = 108000
	nw := int64(runtime.GOMAXPROCS(0))
	if nw < 1 {
		nw = 1
	}
	if nw > total {
		nw = total
	}
	partials := make([]int64, nw)
	chunk := total / nw
	var wg sync.WaitGroup
	for w := int64(0); w < nw; w++ {
		start := w * chunk
		end := (w + 1) * chunk
		if w == nw-1 {
			end = total
		}
		wg.Add(1)
		go func(idx, s, e int64) {
			defer wg.Done()
			var acc int64 = 0
			for i := s; i < e; i++ {
				acc += compute(i)
			}
			partials[idx] = acc
		}(w, start, end)
	}
	wg.Wait()
	var total_sum int64 = 0
	for w := int64(0); w < nw; w++ {
		total_sum += partials[w]
	}
	fmt.Println(total_sum)
}
