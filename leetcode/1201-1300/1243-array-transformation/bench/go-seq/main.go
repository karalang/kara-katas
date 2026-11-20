// LeetCode #1243: the benchmark, mirroring the Kāra file.
package main

import (
	"fmt"
	"slices"
)

func transformArray(arr []int64) []int64 {
	cur := arr
	for {
		next := slices.Clone(cur)
		for i := 1; i < len(cur)-1; i++ {
			if cur[i] < cur[i-1] && cur[i] < cur[i+1] {
				next[i]++
			} else if cur[i] > cur[i-1] && cur[i] > cur[i+1] {
				next[i]--
			}
		}
		if slices.Equal(next, cur) {
			return cur
		}
		cur = next
	}
}

func main() {
	var seed int64 = 1243
	arrays := make([][]int64, 0, 5000)
	for a := 0; a < 5000; a++ {
		arr := make([]int64, 100)
		for i := range arr {
			seed = (seed*1103515245 + 12345) % 2147483648
			arr[i] = seed/65536%100 + 1
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, a := range arrays {
			for _, v := range transformArray(slices.Clone(a)) {
				check = (check*131 + v) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds of 5000 arrays of 100 values: checksum %d\n", check)
}
