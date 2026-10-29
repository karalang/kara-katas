// LeetCode #1009 bench: the ★ arm (an all-ones mask) over 1,000,000 n
// below 10^9, of random lengths, drawn once; each of 50 rounds takes the
// complement of every n plus the round number and folds the round's sum
// into a checksum.
package main

import "fmt"

func bitwiseComplement(n int64) int64 {
	var mask int64 = 1
	for mask < n {
		mask = mask*2 + 1
	}
	return mask ^ n
}

var seed int64 = 1009

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 1000000, 50
	values := make([]int64, count)
	for k := range values {
		bits := 1 + nextRandom()%30
		hi := nextRandom()
		lo := nextRandom()
		values[k] = ((hi*32768 + lo) % (int64(1) << bits)) % 999999000
	}
	var check int64
	for r := 0; r < rounds; r++ {
		var sum int64
		for k := 0; k < count; k++ {
			sum += bitwiseComplement(values[k] + int64(r))
		}
		check = (check*31 + sum) % 1000000007
	}
	fmt.Printf("%d rounds over %d values of n: checksum %d\n", rounds, count, check)
}
