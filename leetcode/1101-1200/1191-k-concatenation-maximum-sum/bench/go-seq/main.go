// LeetCode #1191 bench: the ★ arm in Go, over the same 4 arrays of 10^5
// values and 200 rounds as the Kāra bench.
package main

import "fmt"

func kConcatenationMaxSum(arr []int64, k int64) int64 {
	var total int64
	for _, x := range arr {
		total += x
	}
	var best, run int64
	copies := k
	if copies > 2 {
		copies = 2
	}
	for c := int64(0); c < copies; c++ {
		for _, x := range arr {
			run = max(run+x, 0)
			best = max(best, run)
		}
	}
	if k > 2 && total > 0 {
		best += (k - 2) * total
	}
	return best % 1000000007
}

var seed int64 = 1191

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	random := make([]int64, n)
	lifted := make([]int64, n)
	negative := make([]int64, n)
	alternating := make([]int64, n)
	for i := int64(0); i < n; i++ {
		high := nextRandom()
		low := nextRandom()
		x := (high*32768+low)%20001 - 10000
		random[i] = x
		lifted[i] = min(x+300, 10000)
		if x < 0 {
			negative[i] = x - 1
		} else {
			negative[i] = -x - 1
		}
		if i%2 == 0 {
			alternating[i] = 10000 - i%7
		} else {
			alternating[i] = i%5 - 10000
		}
	}
	arrays := [][]int64{random, lifted, negative, alternating}
	var check int64
	for r := int64(0); r < 200; r++ {
		for _, arr := range arrays {
			check = (check*131 + kConcatenationMaxSum(arr, 100000-r)) % 1000000007
		}
	}
	fmt.Printf("200 rounds of 4 arrays of 100000 values: checksum %d\n", check)
}
