// LeetCode #1465 bench in Go: the ★ arm (each way's cuts sorted and its
// widest gap taken) on the same 100 cakes of 5000 cuts each way and 20
// passes.
package main

import (
	"fmt"
	"slices"
)

func widest(size int32, cuts []int32) int64 {
	sorted := slices.Clone(cuts)
	slices.Sort(sorted)
	best := sorted[0]
	for i := 1; i < len(sorted); i++ {
		best = max(best, sorted[i]-sorted[i-1])
	}
	best = max(best, size-sorted[len(sorted)-1])
	return int64(best)
}

func maxArea(h, w int32, horizontalCuts, verticalCuts []int32) int32 {
	return int32(widest(h, horizontalCuts) * widest(w, verticalCuts) % 1000000007)
}

var seed int64 = 1465

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw() []int32 {
	out := make([]int32, 5000)
	for i := range out {
		r := nextRandom() * 32768
		out[i] = int32(1 + (r+nextRandom())%499999999)
	}
	return out
}

func main() {
	across := make([][]int32, 100)
	down := make([][]int32, 100)
	for c := 0; c < 100; c++ {
		across[c] = draw()
		down[c] = draw()
	}
	var check int64
	for pass := int64(0); pass < 20; pass++ {
		for c := 0; c < 100; c++ {
			h := int32(1000000000 - check%1000)
			w := int32(1000000000 - check/1000%1000)
			got := maxArea(h, w, across[c], down[c])
			check = (check*31 + int64(got) + pass) % 1000000007
		}
	}
	fmt.Printf("20 passes over 100 cakes of 5000 cuts each way: checksum %d\n", check)
}
