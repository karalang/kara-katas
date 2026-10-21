// Benchmark for #829: Consecutive Numbers Sum -- the ★ arm (each length).
//
// Mirrors consecutive_numbers_sum.kara: n has a run of k consecutive
// numbers exactly when n - k * (k - 1) / 2 is a positive multiple of k,
// and k runs while 1 + 2 + ... + k fits.
package main

import "fmt"

func consecutiveNumbersSum(n int64) int64 {
	var count int64
	for k := int64(1); k*(k+1)/2 <= n; k++ {
		if (n-k*(k-1)/2)%k == 0 {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = int64(64), int64(16000)
	seed := int64(829)
	numbers := make([]int64, 0, count)
	for i := int64(0); i < count; i++ {
		a := nextRandom(&seed)
		r := a*32768 + nextRandom(&seed)
		numbers = append(numbers, 500000000+r%500000001)
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		r := consecutiveNumbersSum(numbers[round%count])
		total += r
		checksum = (checksum*131 + r) % 1000000007
	}
	fmt.Printf("%d rounds of %d numbers: total %d, checksum %d\n", rounds, count, total, checksum)
}
