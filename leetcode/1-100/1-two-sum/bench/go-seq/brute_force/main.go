// LeetCode 1 — brute-force O(n²) Two Sum, Go single-threaded mirror.
// Algorithmic peer of bench/brute_force.{kara,rs,c,py}. Same N=5000, K=10,
// sentinel target=-1 (never matches; full O(n²) per call). Stdout sink:
// K * (-1 + -1) = -20.
package main

import "fmt"

func twoSum(nums []int64, target int64) (int, int, bool) {
	n := len(nums)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if nums[i]+nums[j] == target {
				return i, j, true
			}
		}
	}
	return 0, 0, false
}

func main() {
	const N = 5000
	data := make([]int64, N)
	for i := 0; i < N; i++ {
		data[i] = (int64(i) * 7) % 1000
	}

	const target int64 = -1
	var sum int64
	for k := 0; k < 10; k++ {
		if i, j, ok := twoSum(data, target); ok {
			sum += int64(i) + int64(j)
		} else {
			sum += -2
		}
	}
	fmt.Println(sum)
}
