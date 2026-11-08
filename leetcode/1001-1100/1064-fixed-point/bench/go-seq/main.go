// LeetCode #1064: Fixed Point -- the benchmark, the same binary search as
// fixed.kara.
package main

import "fmt"

func fixedPoint(arr []int64) int64 {
	// arr[i] < i for every i below lo, and arr[i] >= i from hi on
	lo, hi := 0, len(arr)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if arr[mid] < int64(mid) {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo < len(arr) && arr[lo] == int64(lo) {
		return int64(lo)
	}
	return -1
}

var seed int64 = 1064

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// `n` distinct numbers in ascending order from `first`, each the last
// plus 1 or 2.
func randomSorted(n, first int64) []int64 {
	arr := make([]int64, 0, n)
	x := first
	for i := int64(0); i < n; i++ {
		arr = append(arr, x)
		x += 1 + nextRandom()%2
	}
	return arr
}

func main() {
	// 8 arrays of 1000000 numbers, built once, then each answered on its
	// first 500000 suffixes
	arrays := [][]int64{}
	for a := int64(0); a < 8; a++ {
		arrays = append(arrays, randomSorted(1000000, -100000*a))
	}
	var calls, found, check int64
	for _, arr := range arrays {
		for p := 0; p < 500000; p++ {
			answer := fixedPoint(arr[p:])
			if answer >= 0 {
				found++
			}
			check = (check*31 + answer + 1) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: %d found, checksum %d\n", calls, found, check)
}
