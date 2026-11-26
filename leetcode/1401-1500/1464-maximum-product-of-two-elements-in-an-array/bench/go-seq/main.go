// LeetCode #1464 bench in Go: the ★ arm (one pass keeping the two largest
// values) on the same 1000 arrays of 500 values and 100 passes.
package main

import "fmt"

func maxProduct(nums []int32) int32 {
	var first, second int32
	for _, x := range nums {
		if x > first {
			second = first
			first = x
		} else if x > second {
			second = x
		}
	}
	return (first - 1) * (second - 1)
}

var seed int64 = 1464

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int32, 1000)
	for p := range arrays {
		arrays[p] = make([]int32, 500)
		for i := range arrays[p] {
			arrays[p][i] = int32(1 + nextRandom()%1000)
		}
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		for p := 0; p < 1000; p++ {
			k := check % 500
			arrays[p][k] = int32(1 + (check/7)%1000)
			got := maxProduct(arrays[p])
			check = (check*31 + int64(got) + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 1000 arrays of 500 values: checksum %d\n", check)
}
