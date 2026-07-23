package main

import "fmt"

func twoSum(arr []int64, target int64) (int64, int64) {
	var lo int64 = 0
	hi := int64(len(arr)) - 1
	for lo < hi {
		sum := arr[lo] + arr[hi]
		if sum == target {
			return lo + 1, hi + 1
		}
		if sum < target {
			lo++
		} else {
			hi--
		}
	}
	return -1, -1 // unreachable — a solution is guaranteed
}

func main() {
	var n, passes int64 = 20000, 20000
	arr := make([]int64, n)
	var state int64 = 12345
	var val int64 = 0
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		val += 1 + (state % 3)
		arr[c] = val
	}
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		a := state % n
		state = (state*1103515245 + 12345) & 2147483647
		b := state % n
		if a == b {
			b = (a + 1) % n
		}
		target := arr[a] + arr[b]
		lo, hi := twoSum(arr, target)
		sink += lo + hi
	}
	fmt.Println(sink)
}
