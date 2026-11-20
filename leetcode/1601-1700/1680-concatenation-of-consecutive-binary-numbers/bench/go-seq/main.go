// LeetCode #1680: Concatenation of Consecutive Binary Numbers -- the bench's
// Go mirror: the ★ arm on 800 random n up to 100000, all drawn first, each
// answered 5 times.

package main

import "fmt"

func concatenatedBinary(n int32) int32 {
	const modulus = 1000000007
	var value int64
	bits := 0
	for i := int64(1); i <= int64(n); i++ {
		if i&(i-1) == 0 {
			bits++
		}
		value = ((value << bits) + i) % modulus
	}
	return int32(value)
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1680

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 800
	const rounds = 5
	ns := make([]int32, count)
	for c := range ns {
		ns[c] = int32((nextRandom()*32768+nextRandom())%100000 + 1)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range ns {
			answer := int64(concatenatedBinary(n))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d values of n, %d rounds: answers sum to %d, checksum %d\n", count, rounds, total, check)
}
