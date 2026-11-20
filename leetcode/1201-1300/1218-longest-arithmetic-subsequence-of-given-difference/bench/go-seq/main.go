// LeetCode #1218 bench, in Go: the ★ arm (a map from each value to the
// longest subsequence ending with it) on 16 arrays of 10^5 values from
// -10^4 to 10^4 drawn once, each asked with the differences -3 to 3;
// every answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1218

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func longestSubsequence(arr []int64, difference int64) int64 {
	ending := map[int64]int64{}
	var best int64
	for _, x := range arr {
		length := ending[x-difference] + 1
		ending[x] = length
		if length > best {
			best = length
		}
	}
	return best
}

func main() {
	arrays := make([][]int64, 16)
	for a := range arrays {
		arr := make([]int64, 100000)
		for i := range arr {
			arr[i] = nextRandom()%20001 - 10000
		}
		arrays[a] = arr
	}
	var check int64
	for _, arr := range arrays {
		for d := int64(-3); d <= 3; d++ {
			check = (check*131 + longestSubsequence(arr, d) + d + 3) % 1000000007
		}
	}
	fmt.Printf("16 arrays of 10^5 values, differences -3 to 3: checksum %d\n", check)
}
