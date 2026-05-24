// LeetCode 153 — binary-search find-min, Go single-threaded mirror.
// Algorithmic peer of bench/binary_search.{kara,rs,c,py}. N=2_000_000,
// R=666_666, K=2_000_000. Stdout sink: 2000000.
package main

import "fmt"

//go:noinline
func blackBox[T any](v T) T { return v }

func findMin(nums []int64) int64 {
	lo := 0
	hi := len(nums) - 1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > nums[hi] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return nums[lo]
}

func main() {
	const N = 2_000_000
	const R = 666_666
	const K = 2_000_000

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
