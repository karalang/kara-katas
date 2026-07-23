package main

import "fmt"

func absI64(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func bucketOf(x, w int64) int64 {
	if x >= 0 {
		return x / w
	}
	return (x+1)/w - 1
}

func nearValue(m map[int64]int64, b, x, t int64) bool {
	if v, ok := m[b]; ok {
		if absI64(x-v) <= t {
			return true
		}
	}
	return false
}

func contains(nums []int64, n, k, t int64) bool {
	if k <= 0 {
		return false
	}
	w := t + 1
	buckets := make(map[int64]int64)
	for i := int64(0); i < n; i++ {
		x := nums[i]
		b := bucketOf(x, w)
		if nearValue(buckets, b, x, t) {
			return true
		}
		if nearValue(buckets, b-1, x, t) {
			return true
		}
		if nearValue(buckets, b+1, x, t) {
			return true
		}
		buckets[b] = x
		if i >= k {
			old := nums[i-k]
			delete(buckets, bucketOf(old, w))
		}
	}
	return false
}

func main() {
	var n int64 = 20000
	var pairs int64 = 800
	var valrange int64 = 8000000
	var half int64 = 4000000

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		nums = append(nums, (state%valrange)-half)
	}

	var sink int64 = 0
	for p := int64(0); p < pairs; p++ {
		k := 32 + (p % 512)
		t := p % 3
		if contains(nums, n, k, t) {
			sink++
		}
	}
	fmt.Println(sink)
}
