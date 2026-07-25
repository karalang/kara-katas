// Benchmark harness for LeetCode #347 — scalar-keyed Map approach.
// Mirrors top_k_frequent.kara algorithm-for-algorithm.
package main

import "fmt"

func topKFrequent(nums []int64, k int64) []int64 {
	counts := make(map[int64]int64)
	for _, v := range nums {
		counts[v] = counts[v] + 1
	}

	vals := make([]int64, 0, len(counts))
	for v := range counts {
		vals = append(vals, v)
	}

	for a := 1; a < len(vals); a++ {
		cur := vals[a]
		curC := counts[cur]
		b := a - 1
		for b >= 0 {
			prev := vals[b]
			prevC := counts[prev]
			shift := false
			if prevC < curC {
				shift = true
			}
			if prevC == curC && prev > cur {
				shift = true
			}
			if !shift {
				break
			}
			vals[b+1] = prev
			b--
		}
		vals[b+1] = cur
	}

	limit := int(k)
	if len(vals) < limit {
		limit = len(vals)
	}
	out := make([]int64, 0, limit)
	for t := 0; t < limit; t++ {
		out = append(out, vals[t])
	}
	return out
}

const (
	N     = 8000
	D     = 200
	Iters = 300
	K     = 10
)

func main() {
	bs := make([]int64, N)
	for i := int64(0); i < N; i++ {
		v := i % D
		if i%5 == 0 {
			v = i % 13
		}
		bs[i] = v
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		p := (it * 7919) % N
		bs[p] = (it * 37) % D
		got := topKFrequent(bs, K)
		for _, v := range got {
			sink += v
		}
	}
	fmt.Println(sink)
}
