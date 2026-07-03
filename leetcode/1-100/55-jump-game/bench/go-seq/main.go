// LeetCode #55 bench mirror — Go, the greedy forward max-reach solver (★).
//
// Mirrors bench/jump_game.kara: one left-to-right scan with a single `farthest` scalar, deciding
// reachability and returning the index it decided at. Build a reachable array once, punch one
// slot per iteration, fold the decision index into a rolling checksum. Same workload + sink as
// every other mirror.
package main

import "fmt"

func canJumpWork(nums []int64, n int64) int64 {
	var farthest int64 = 0
	var i int64 = 0
	for i < n {
		if i > farthest {
			return i
		}
		if i+nums[i] > farthest {
			farthest = i + nums[i]
		}
		if farthest >= n-1 {
			return i
		}
		i++
	}
	return i
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
		ans := canJumpWork(nums, n)
		acc = (acc*131 + ans) % modulus
	}

	fmt.Println(acc)
}
