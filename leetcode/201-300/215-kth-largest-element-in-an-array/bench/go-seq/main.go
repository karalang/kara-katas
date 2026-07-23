package main

import "fmt"

func partition(a []int64, lo, hi int64) int64 {
	pivot := a[hi]
	i := lo
	j := lo
	for j < hi {
		if a[j] < pivot {
			a[i], a[j] = a[j], a[i]
			i++
		}
		j++
	}
	a[i], a[hi] = a[hi], a[i]
	return i
}

func quickselect(a []int64, lo, hi, target int64) int64 {
	if lo == hi {
		return a[lo]
	}
	p := partition(a, lo, hi)
	if p == target {
		return a[p]
	}
	if target < p {
		return quickselect(a, lo, p-1, target)
	}
	return quickselect(a, p+1, hi, target)
}

func main() {
	var n, passes, k int64 = 120000, 420, 40000
	target := n - k

	a := make([]int64, n)
	var state int64 = 12345
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		for i := int64(0); i < n; i++ {
			state = (state*1103515245 + 12345) & 2147483647
			a[i] = state
		}
		sink += quickselect(a, 0, n-1, target)
	}
	fmt.Println(sink)
}
