// LeetCode #1588: Sum of All Odd Length Subarrays -- the bench in Go,
// mirroring odd_subarrays.kara.
package main

import "fmt"

func sumOddLengthSubarrays(arr []int32) int32 {
	n := int64(len(arr))
	var total int32
	for i, v := range arr {
		i := int64(i)
		through := (i + 1) * (n - i)
		total += int32((through+1)/2) * v
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1588)
	arrays := make([][]int32, 0)
	for k := 0; k < 200000; k++ {
		n := nextRandom(&seed)%100 + 1
		arr := make([]int32, n)
		for i := range arr {
			arr[i] = int32(nextRandom(&seed)%1000 + 1)
		}
		arrays = append(arrays, arr)
	}
	var check, total int64
	for _, arr := range arrays {
		answer := int64(sumOddLengthSubarrays(arr))
		total += answer
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("200000 arrays of 1 to 100 values: total %d, checksum %d\n", total, check)
}
