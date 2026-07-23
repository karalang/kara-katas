package main

import "fmt"

func findPeak(arr []int64, lo, hi int64) int64 {
	for lo < hi {
		mid := lo + (hi-lo)/2
		if arr[mid] < arr[mid+1] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	var n, window, passes int64 = 4000000, 4096, 1000000
	arr := make([]int64, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		arr[c] = state % 1000003
	}
	span := n - window
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		base := (p * 4099) % span
		arr[base] = (arr[base] + 1) % 1000003
		sink += findPeak(arr, base, base+window-1)
	}
	fmt.Println(sink)
}
