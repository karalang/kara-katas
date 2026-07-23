package main

import "fmt"

func numDigits(x int64) int64 {
	var d int64 = 1
	t := x
	for t >= 10 {
		d++
		t /= 10
	}
	return d
}

func pow10(k int64) int64 {
	var r int64 = 1
	for i := int64(0); i < k; i++ {
		r *= 10
	}
	return r
}

func concatVal(a, b int64) int64 {
	return a*pow10(numDigits(b)) + b
}

func sortDesc(arr []int64, n int64) {
	for i := int64(1); i < n; i++ {
		j := i
		for j > 0 && concatVal(arr[j-1], arr[j]) < concatVal(arr[j], arr[j-1]) {
			arr[j-1], arr[j] = arr[j], arr[j-1]
			j--
		}
	}
}

func checksum(arr []int64, n int64) int64 {
	var modv int64 = 1000000007
	var cs int64 = 0
	for i := int64(0); i < n; i++ {
		x := arr[i]
		p := pow10(numDigits(x) - 1)
		for p > 0 {
			d := (x / p) % 10
			cs = (cs*10 + d) % modv
			p /= 10
		}
	}
	return cs
}

func main() {
	var n, passes int64 = 500, 400
	base := make([]int64, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		base[c] = state % 1000
	}
	arr := make([]int64, n)
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		copy(arr, base)
		idx := p % n
		arr[idx] = (arr[idx] + p + 1) % 1000
		sortDesc(arr, n)
		sink += checksum(arr, n)
	}
	fmt.Println(sink)
}
