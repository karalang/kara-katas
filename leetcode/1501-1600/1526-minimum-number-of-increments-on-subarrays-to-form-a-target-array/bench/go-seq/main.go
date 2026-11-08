// LeetCode #1526: Minimum Number of Increments on Subarrays to Form a
// Target Array -- bench: the ★ arm over 100 random arrays of 1 to 100000 numbers up to 10000, built once and answered 50 times.
package main

import "fmt"

func minNumberOperations(target []int64) int64 {
	total := target[0]
	for i := 1; i < len(target); i++ {
		if target[i] > target[i-1] {
			total += target[i] - target[i-1]
		}
	}
	return total
}

var seed int64 = 1526

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
		target := make([]int64, 0)
		for i := int64(0); i < n; i++ {
			hi = nextRandom()
			target = append(target, (hi*32768+nextRandom())%10000+1)
		}
		arrays = append(arrays, target)
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		for _, target := range arrays {
			check = mix(check, minNumberOperations(target))
		}
	}
	fmt.Printf("50 passes over 100 arrays of up to 100000 numbers: checksum %d\n", check)
}
