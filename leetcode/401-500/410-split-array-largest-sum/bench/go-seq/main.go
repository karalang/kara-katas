// Benchmark for #410: mirror of split_array.kara (binary search on the
// answer).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func piecesNeeded(nums []int64, cap int64) int64 {
	var pieces int64 = 1
	var sum int64
	for i := 0; i < len(nums); i++ {
		if sum+nums[i] > cap {
			pieces++
			sum = nums[i]
		} else {
			sum += nums[i]
		}
	}
	return pieces
}

func splitArray(nums []int64, k int64) int64 {
	var lo, hi int64
	for i := 0; i < len(nums); i++ {
		if nums[i] > lo {
			lo = nums[i]
		}
		hi += nums[i]
	}
	for lo < hi {
		mid := lo + (hi-lo)/2
		if piecesNeeded(nums, mid) <= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

var seed int64 = 410

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var arrays int64 = 10000
	if len(os.Args) > 1 {
		arrays, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	n := 1000
	var total, checksum int64
	for t := int64(0); t < arrays; t++ {
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			hi := step()
			lo := step()
			nums = append(nums, (hi*32768+lo)%1000001)
		}
		k := 1 + step()%50
		answer := splitArray(nums, k)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d arrays of %d numbers: total %d, checksum %d\n", arrays, n, total, checksum)
}
