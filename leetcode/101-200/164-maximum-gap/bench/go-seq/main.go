// LeetCode 164 — Maximum Gap benchmark kernel (Go mirror, go build).
//
// Build-once + punch: LCG-filled N values, maximumGap called K times with a
// one-element perturbation each round. Sink = sum of the K gaps. Identical
// algorithm to the Kāra / C / Rust / Python mirrors.
package main

import "fmt"

func maximumGap(nums []int64) int64 {
	n := int64(len(nums))
	if n < 2 {
		return 0
	}
	lo, hi := nums[0], nums[0]
	for i := int64(1); i < n; i++ {
		if nums[i] < lo {
			lo = nums[i]
		}
		if nums[i] > hi {
			hi = nums[i]
		}
	}
	if lo == hi {
		return 0
	}

	bsize := (hi - lo) / (n - 1)
	if bsize < 1 {
		bsize = 1
	}
	bcount := (hi-lo)/bsize + 1

	used := make([]bool, bcount)
	bmin := make([]int64, bcount)
	bmax := make([]int64, bcount)

	for _, x := range nums {
		idx := (x - lo) / bsize
		if used[idx] {
			if x < bmin[idx] {
				bmin[idx] = x
			}
			if x > bmax[idx] {
				bmax[idx] = x
			}
		} else {
			bmin[idx] = x
			bmax[idx] = x
			used[idx] = true
		}
	}

	var gap int64 = 0
	prevMax := lo
	for b := int64(0); b < bcount; b++ {
		if used[b] {
			if bmin[b]-prevMax > gap {
				gap = bmin[b] - prevMax
			}
			prevMax = bmax[b]
		}
	}
	return gap
}

func main() {
	const n int64 = 1000000
	const k int64 = 30
	const rng int64 = 1000000000

	nums := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		nums[i] = state % rng
	}

	var sink int64 = 0
	for round := int64(0); round < k; round++ {
		idx := (round * 7919) % n
		nums[idx] = (nums[idx] + 1 + round) % rng
		sink += maximumGap(nums)
	}
	fmt.Println(sink)
}
