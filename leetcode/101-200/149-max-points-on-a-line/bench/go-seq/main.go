// LeetCode 149 — Max Points on a Line, sort-based Go seq mirror.
package main

import (
	"fmt"
	"sort"
)

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func abs64(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func maxPoints(xs, ys []int64) int64 {
	n := int64(len(xs))
	if n <= 2 {
		return n
	}
	best := int64(1)
	slopes := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		slopes = slopes[:0]
		dup := int64(0)
		for j := i + 1; j < n; j++ {
			dx := xs[j] - xs[i]
			dy := ys[j] - ys[i]
			if dx == 0 && dy == 0 {
				dup++
				continue
			}
			g := gcd(abs64(dx), abs64(dy))
			dx /= g
			dy /= g
			if dx < 0 || (dx == 0 && dy < 0) {
				dx = -dx
				dy = -dy
			}
			slopes = append(slopes, dx*4096+dy)
		}
		sort.Slice(slopes, func(a, b int) bool { return slopes[a] < slopes[b] })
		var local, run int64
		for k := 0; k < len(slopes); k++ {
			if k == 0 || slopes[k] != slopes[k-1] {
				run = 1
			} else {
				run++
			}
			if run > local {
				local = run
			}
		}
		if cand := local + dup + 1; cand > best {
			best = cand
		}
	}
	return best
}

func main() {
	const N = 1200
	xs := make([]int64, N)
	ys := make([]int64, N)
	state := int64(12345)
	for i := 0; i < N; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		xs[i] = state & 1023
		state = (state*1103515245 + 12345) & 2147483647
		ys[i] = state & 1023
	}
	var sum int64
	for k := 0; k < 8; k++ {
		sum += maxPoints(xs, ys)
	}
	fmt.Println(sum)
}
