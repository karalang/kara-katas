// LeetCode #1534: Count Good Triplets -- bench: the ★ arm over 100 random
// arrays of 100 values up to 1000, each with its own a, b and c up to
// 1000, built once and answered 10 times. Go mirror of triplets.kara.
package main

import "fmt"

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func countGoodTriplets(arr []int64, a, b, c int64) int64 {
	n := len(arr)
	var count int64
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if abs(arr[i]-arr[j]) > a {
				continue
			}
			for k := j + 1; k < n; k++ {
				if abs(arr[j]-arr[k]) <= b && abs(arr[i]-arr[k]) <= c {
					count++
				}
			}
		}
	}
	return count
}

var seed int64 = 1534

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type tcase struct {
	arr     []int64
	a, b, c int64
}

func main() {
	cases := make([]tcase, 0, 100)
	for p := 0; p < 100; p++ {
		arr := make([]int64, 100)
		for i := range arr {
			arr[i] = nextRandom() % 1001
		}
		a := nextRandom() % 1001
		b := nextRandom() % 1001
		c := nextRandom() % 1001
		cases = append(cases, tcase{arr, a, b, c})
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, t := range cases {
			check = mix(check, countGoodTriplets(t.arr, t.a, t.b, t.c))
		}
	}
	fmt.Printf("10 passes over 100 arrays of 100 values: checksum %d\n", check)
}
