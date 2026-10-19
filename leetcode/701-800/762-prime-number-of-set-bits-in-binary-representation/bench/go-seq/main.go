// LeetCode 762 — Prime Number of Set Bits in Binary Representation:
// benchmark, the ★ arm in Go.
package main

import "fmt"

func countPrimeSetBits(left, right int64) int64 {
	var count int64
	for n := left; n <= right; n++ {
		bits := 0
		for rest := n; rest > 0; rest &= rest - 1 {
			bits++
		}
		switch bits {
		case 2, 3, 5, 7, 11, 13, 17, 19:
			count++
		}
	}
	return count
}

var seed int64 = 762

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 10000
	var total, check int64
	for r := 0; r < rounds; r++ {
		high := nextRandom()
		left := 1 + (high*32768+nextRandom())%990000
		count := countPrimeSetBits(left, left+10000)
		total += count
		check = (check*31 + count) % 1000000007
	}
	fmt.Printf("%d ranges of 10001 numbers: %d counted, checksum %d\n", rounds, total, check)
}
