// LeetCode #1524: Number of Sub-arrays With Odd Sum -- bench: the ★ arm
// over 100 random arrays of 1 to 100000 numbers from 1 to 100, built once
// and answered 20 times.
package main

import "fmt"

func numOfSubarrays(arr []int64) int64 {
	const modulus = 1000000007
	var odd, sum, answer int64
	even := int64(1)
	for _, x := range arr {
		sum += x
		if sum%2 == 1 {
			answer = (answer + even) % modulus
			odd++
		} else {
			answer = (answer + odd) % modulus
			even++
		}
	}
	return answer
}

var seed int64 = 1524

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	arrays := make([][]int64, 0, 100)
	for c := 0; c < 100; c++ {
		hi := nextRandom()
		n := (hi*32768+nextRandom())%100000 + 1
		arr := make([]int64, 0)
		for i := int64(0); i < n; i++ {
			arr = append(arr, nextRandom()%100+1)
		}
		arrays = append(arrays, arr)
	}
	var check int64
	for pass := 0; pass < 20; pass++ {
		for _, arr := range arrays {
			check = mix(check, numOfSubarrays(arr))
		}
	}
	fmt.Printf("20 passes over 100 arrays of up to 100000 numbers: checksum %d\n", check)
}
