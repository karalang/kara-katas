// LeetCode #1343 bench in Go: the ★ arm (a sliding window of the last k
// values, counted when its sum reaches k * threshold) on the same 10
// arrays of 10^5 values and 60 passes.
package main

import "fmt"

func numOfSubarrays(arr []int32, k, threshold int32) int32 {
	need := k * threshold
	var sum, count int32
	for i := range arr {
		sum += arr[i]
		if int32(i) >= k {
			sum -= arr[int32(i)-k]
		}
		if int32(i) >= k-1 && sum >= need {
			count++
		}
	}
	return count
}

var seed int64 = 1343

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(100000)
	arrays := make([][]int32, 10)
	for a := range arrays {
		arrays[a] = make([]int32, n)
		for i := range arrays[a] {
			arrays[a][i] = int32(1 + nextRandom()%10000)
		}
	}
	var check int64
	for pass := int64(0); pass < 60; pass++ {
		for a := 0; a < 10; a++ {
			arrays[a][check%n] = int32(1 + (check/7)%10000)
			k := int32(1 + check%1000)
			threshold := int32(4500 + check%400)
			answer := numOfSubarrays(arrays[a], k, threshold)
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("60 passes over 10 arrays of 10^5: checksum %d\n", check)
}
