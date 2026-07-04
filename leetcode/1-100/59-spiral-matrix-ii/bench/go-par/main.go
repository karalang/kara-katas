// LeetCode #59 — Go goroutine-parallel mirror (par lane, spiral_matrix_ii).
// Same boundary-shrinking generator + position-weighted checksum; the K=180k
// reduction is split across NumCPU workers (per-worker partial + sum).
// Hand-tuned-parallel comparator. Sink matches the kara/rust/c/go mirrors.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	mSizes = 9
	kIters = 180000
)

func generateMatrix(n int64) [][]int64 {
	grid := make([][]int64, n)
	for r := int64(0); r < n; r++ {
		grid[r] = make([]int64, n)
	}
	top, bottom, left, right, v := int64(0), n-1, int64(0), n-1, int64(1)
	for top <= bottom && left <= right {
		for c := left; c <= right; c++ {
			grid[top][c] = v
			v++
		}
		top++
		for r2 := top; r2 <= bottom; r2++ {
			grid[r2][right] = v
			v++
		}
		right--
		if top <= bottom {
			for c2 := right; c2 >= left; c2-- {
				grid[bottom][c2] = v
				v++
			}
			bottom--
		}
		if left <= right {
			for r3 := bottom; r3 >= top; r3-- {
				grid[r3][left] = v
				v++
			}
			left++
		}
	}
	return grid
}

func checksum(grid [][]int64, n int64) int64 {
	var s int64 = 0
	for i := int64(0); i < n; i++ {
		for j := int64(0); j < n; j++ {
			s += grid[i][j] * (i*n + j + 1)
		}
	}
	return s
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
				n := 12 + (k % mSizes)
				g := generateMatrix(n)
				s += checksum(g, n)
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
