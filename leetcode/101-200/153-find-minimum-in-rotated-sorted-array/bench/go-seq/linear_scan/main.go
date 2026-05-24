// LeetCode 153 — linear-scan find-min, Go single-threaded mirror.
// Algorithmic peer of bench/linear_scan.{kara,rs,c,py}. N=2_000_000, R=666_666,
// K=10. Stdout sink: 10.
package main

import "fmt"

//go:noinline
func blackBox[T any](v T) T { return v }

func findMin(nums []int64) int64 {
	m := nums[0]
	for i := 1; i < len(nums); i++ {
		if nums[i] < m {
			m = nums[i]
		}
	}
	return m
}

func main() {
	const N = 2_000_000
	const R = 666_666
	const K = 10

	data := make([]int64, N)
	for i := 0; i < N; i++ {
		data[i] = int64(((i+R)%N)+1)
	}

	var sum int64
	for k := 0; k < K; k++ {
		sum += findMin(blackBox(data))
	}
	fmt.Println(sum)
}
