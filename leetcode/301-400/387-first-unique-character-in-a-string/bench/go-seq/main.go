// Benchmark harness for LeetCode #387 — Map (general-alphabet) approach.
// Mirrors first_unique_char.kara algorithm-for-algorithm.
package main

import "fmt"

func firstUniqChar(bs []int64) int64 {
	counts := make(map[int64]int64)
	for _, c := range bs {
		counts[c] = counts[c] + 1
	}

	for j, c := range bs {
		if counts[c] == 1 {
			return int64(j)
		}
	}
	return -1
}

func uniqueCount(bs []int64) int64 {
	counts := make(map[int64]int64)
	for _, c := range bs {
		counts[c] = counts[c] + 1
	}
	var uniq int64
	for k := range counts {
		if counts[k] == 1 {
			uniq++
		}
	}
	return uniq
}

const (
	N     = 4000
	Iters = 2000
)

func main() {
	bs := make([]int64, N)
	for i := int64(0); i < N; i++ {
		bs[i] = 97 + (i % 25)
	}
	bs[N-1] = 122

	var sink int64
	for it := int64(0); it < Iters; it++ {
		p := (it * 7919) % N
		bs[p] = 97 + (it % 25)
		sink += firstUniqChar(bs)
		sink += uniqueCount(bs)
	}
	fmt.Println(sink)
}
