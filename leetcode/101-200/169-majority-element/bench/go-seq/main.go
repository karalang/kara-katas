// LeetCode 169 — Majority Element benchmark kernel (Go mirror, go build).
//
// Build-once + punch: LCG-filled N values with a 60% majority, Boyer-Moore scan
// run K times with a one-element perturbation each round. Sink = sum of the K
// results. Identical algorithm to the Kāra / C / Rust / Python mirrors.
package main

import "fmt"

func majorityElement(nums []int64) int64 {
	candidate := nums[0]
	var count int64 = 0
	for _, x := range nums {
		if count == 0 {
			candidate = x
		}
		if x == candidate {
			count++
		} else {
			count--
		}
	}
	return candidate
}

func main() {
	const n int64 = 10000000
	const k int64 = 20
	const majority int64 = 7

	nums := make([]int64, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) % 2147483648
		if state%100 < 60 {
			nums[i] = majority
		} else {
			nums[i] = state%1000000 + 1000
		}
	}

	var sink int64 = 0
	for round := int64(0); round < k; round++ {
		idx := (round * 7919) % n
		nums[idx] = nums[idx] + 1
		sink += majorityElement(nums)
	}
	fmt.Println(sink)
}
