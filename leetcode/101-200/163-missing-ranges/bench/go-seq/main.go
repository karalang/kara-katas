package main

import "fmt"

func missingRanges(arr []int64, start, length, lower, upper int64) (int64, int64) {
	var count int64 = 0
	var checksum int64 = 0
	prev := lower - 1
	for i := int64(0); i <= length; i++ {
		var cur int64
		if i < length {
			cur = arr[start+i]
		} else {
			cur = upper + 1
		}
		if cur-prev >= 2 {
			count++
			checksum += (prev + 1) + (cur - 1)
		}
		prev = cur
	}
	return count, checksum
}

func main() {
	var n, window, passes int64 = 1000000, 2000, 120000
	arr := make([]int64, n)
	var state int64 = 12345
	var val int64 = 0
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		val += 1 + (state % 3)
		arr[c] = val
	}
	span := n - window
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		start := (p * 7919) % span
		lower := arr[start]
		upper := arr[start+window-1] + (p % 5)
		count, checksum := missingRanges(arr, start, window, lower, upper)
		sink += count + checksum
	}
	fmt.Println(sink)
}
