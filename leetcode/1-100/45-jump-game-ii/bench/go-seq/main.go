// LeetCode #45 bench mirror — Go, the greedy range-expansion matcher (★).
//
// Mirrors bench/jump_game_ii.kara: one cursor with farthest/current_end/jumps scalars,
// collapsing the layered BFS into a single scan. Build a reachable array once, punch one slot
// per iteration, fold the jump count into a rolling checksum. Same workload + sink as every
// other mirror.
package main

import "fmt"

func jump(nums []int64, n int64) int64 {
	var jumps, currentEnd, farthest int64 = 0, 0, 0
	for i := int64(0); i < n-1; i++ {
		if i+nums[i] > farthest {
			farthest = i + nums[i]
		}
		if i == currentEnd {
			jumps++
			currentEnd = farthest
		}
	}
	return jumps
}

func main() {
	var total int64 = 200000
	var modulus int64 = 1000000007
	var n int64 = 1000

	nums := make([]int64, n)
	for a := int64(0); a < n; a++ {
		nums[a] = 1 + (a % 4)
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		nums[k%n] = 1 + (k % 9)
		ans := jump(nums, n)
		acc = (acc*131 + ans) % modulus
	}

	fmt.Println(acc)
}
