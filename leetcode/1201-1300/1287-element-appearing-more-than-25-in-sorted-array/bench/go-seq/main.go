// LeetCode #1287 bench, in Go: the ★ arm (the first i where arr[i] equals
// arr[i + n / 4]) on 100 sorted arrays of 10^5 numbers, built once, 1000
// rounds, every answer folded into a checksum.
package main

import (
	"fmt"
	"sort"
)

func findSpecialInteger(arr []int64) int64 {
	quarter := len(arr) / 4
	for i := 0; i < len(arr)-quarter; i++ {
		if arr[i] == arr[i+quarter] {
			return arr[i]
		}
	}
	return -1
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func problem(n int64) []int64 {
	planted := nextRandom() % 100001
	times := n/4 + 1 + nextRandom()%(n/4)
	arr := make([]int64, 0, n)
	for int64(len(arr)) < times {
		arr = append(arr, planted)
	}
	for int64(len(arr)) < n {
		x := nextRandom() % 100001
		if x != planted {
			arr = append(arr, x)
		}
	}
	sort.Slice(arr, func(i, j int) bool { return arr[i] < arr[j] })
	return arr
}

func main() {
	seed = 1287
	problems := make([][]int64, 0)
	for k := 0; k < 100; k++ {
		problems = append(problems, problem(100000))
	}
	var check int64
	for round := int64(0); round < 1000; round++ {
		for _, arr := range problems {
			check = (check*131 + findSpecialInteger(arr) + round) % 1000000007
		}
	}
	fmt.Printf("1000 rounds of 100 arrays of 100000 numbers: checksum %d\n", check)
}
