// LeetCode #1122: Relative Sort Array -- the bench in Go: the ★ arm over
// 4 problems of 1000 values, each round swapping two values of each `arr1`
// and two of each `arr2` and sorting it again.
package main

import (
	"fmt"
	"sort"
)

var seed int64 = 1122

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func relativeSortArray(arr1, arr2 []int32) []int32 {
	var count [1001]int64
	for _, x := range arr1 {
		count[x]++
	}
	out := make([]int32, 0, len(arr1))
	for _, x := range arr2 {
		for c := int64(0); c < count[x]; c++ {
			out = append(out, x)
		}
		count[x] = 0
	}
	for v := 0; v < 1001; v++ {
		for c := int64(0); c < count[v]; c++ {
			out = append(out, int32(v))
		}
	}
	return out
}

func main() {
	tops := []int64{1000, 500, 100, 10}
	var ones, twos [][]int32
	for _, top := range tops {
		arr1 := make([]int32, 1000)
		for i := range arr1 {
			arr1[i] = int32(nextRandom() % (top + 1))
		}
		sorted := append([]int32(nil), arr1...)
		sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
		var distinct []int32
		for i, x := range sorted {
			if i == 0 || sorted[i-1] != x {
				distinct = append(distinct, x)
			}
		}
		for j := len(distinct) - 1; j >= 1; j-- {
			k := nextRandom() % int64(j+1)
			distinct[j], distinct[k] = distinct[k], distinct[j]
		}
		twos = append(twos, append([]int32(nil), distinct[:(len(distinct)+1)/2]...))
		ones = append(ones, arr1)
	}
	var check int64
	for round := 0; round < 5000; round++ {
		for j := 0; j < 4; j++ {
			a, t := ones[j], twos[j]
			m := len(t)
			p, q := round*7919%1000, round*104729%1000
			a[p], a[q] = a[q], a[p]
			p, q = round*31%m, round*17%m
			t[p], t[q] = t[q], t[p]
			for _, x := range relativeSortArray(a, t) {
				check = (check*31 + int64(x)) % 1000000007
			}
		}
	}
	fmt.Printf("5000 rounds over 4 problems of 1000 values: checksum %d\n", check)
}
