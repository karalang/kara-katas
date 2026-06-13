// LeetCode #3629 — Go goroutine-parallel mirror (par lane, bfs_sieve).
// Same BFS + prime-factor-sieve min_jumps; the K=50-call reduction split across
// NumCPU workers (per-worker partial + merge). Hand-tuned-parallel comparator
// for Kāra's auto-par. Sink = 24350 (K=50 × per-call result 487). The input
// slice is shared read-only across goroutines; minJumps allocates its own
// factors/bucket/visited per call.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

const (
	n     = 50000
	iters = 50
)

func buildFactors(cap int64) [][]int64 {
	factors := make([][]int64, cap+1)
	for i := int64(2); i <= cap; i++ {
		if len(factors[i]) == 0 {
			for j := i; j <= cap; j += i {
				factors[j] = append(factors[j], i)
			}
		}
	}
	return factors
}

func minJumps(nums []int64) int64 {
	nn := int64(len(nums))
	if nn <= 1 {
		return 0
	}
	cap := int64(1)
	for _, v := range nums {
		if v > cap {
			cap = v
		}
	}
	factors := buildFactors(cap)

	bucket := make(map[int64][]int64)
	for j, v := range nums {
		if v >= 2 {
			for _, p := range factors[v] {
				bucket[p] = append(bucket[p], int64(j))
			}
		}
	}

	visited := make([]bool, nn)
	visited[0] = true

	type node struct{ i, d int64 }
	queue := []node{{0, 0}}
	head := 0
	for head < len(queue) {
		cur := queue[head]
		head++
		i, d := cur.i, cur.d
		if i == nn-1 {
			return d
		}
		if i > 0 && !visited[i-1] {
			visited[i-1] = true
			queue = append(queue, node{i - 1, d + 1})
		}
		if i+1 < nn && !visited[i+1] {
			visited[i+1] = true
			queue = append(queue, node{i + 1, d + 1})
		}
		v := nums[i]
		if v >= 2 && factors[v][0] == v {
			if indices, ok := bucket[v]; ok {
				delete(bucket, v)
				for _, j := range indices {
					if !visited[j] {
						visited[j] = true
						queue = append(queue, node{j, d + 1})
					}
				}
			}
		}
	}
	return -1
}

func main() {
	data := make([]int64, n)
	for i := 0; i < n; i++ {
		data[i] = (int64(i)*7919 + 13) % 999983 + 2
	}

	workers := runtime.NumCPU()
	if workers > iters {
		workers = iters
	}
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
			for k := start; k < end; k++ {
				s += minJumps(data)
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
