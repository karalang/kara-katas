// LeetCode #11 — Go seq bench peer for container.kara. Same two-pointer
// matcher, same workload (N=8, W=16, K=10M), same sink as the Kara /
// Rust / C mirrors.

package main

import "fmt"

func maxAreaOff(heights []int64, lo int64, hi int64) int64 {
	l := lo
	r := hi
	var best int64 = 0
	for l < r {
		hL := heights[l]
		hR := heights[r]
		var h int64
		if hL < hR {
			h = hL
		} else {
			h = hR
		}
		area := h * (r - l)
		if area > best {
			best = area
		}
		if hL < hR {
			l += 1
		} else {
			r -= 1
		}
	}
	return best
}

func main() {
	const n int64 = 8
	const w int64 = 16
	const total int64 = n * w
	const kIters int64 = 10_000_000

	heights := make([]int64, total)
	for i := int64(0); i < total; i++ {
		raw := i*2654435769 + 305419896
		v := ((raw % 50) + 50) % 50
		heights[i] = v
	}

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		lo := idx * w
		hi := lo + w - 1
		sum += maxAreaOff(heights, lo, hi)
	}
	fmt.Println(sum)
}
