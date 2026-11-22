// LeetCode #2749: Minimum Operations to Make the Integer Zero -- the
// bench (zero.kara in Go): the least k with t = num1 - k num2 a sum of k
// powers of two, by `bits.OnesCount64`.
package main

import (
	"fmt"
	"math/bits"
)

func makeTheIntegerZero(num1, num2 int64) int64 {
	for k := int64(1); k <= 60; k++ {
		t := num1 - k*num2
		if int64(bits.OnesCount64(uint64(t))) <= k && k <= t {
			return k
		}
	}
	return -1
}

var seed int64 = 2749

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 1000000, 10
	pairs := make([][2]int64, count)
	for i := range pairs {
		hi := nextRandom()
		num1 := (hi*32768+nextRandom())%1000000000 + 1
		hi = nextRandom()
		size := (hi*32768 + nextRandom()) % 1000000001
		num2 := size
		if nextRandom()%2 != 0 {
			num2 = -size
		}
		pairs[i] = [2]int64{num1, num2}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range pairs {
			steps := makeTheIntegerZero(p[0], p[1])
			sum += steps
			check = (check*31 + steps + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs, %d rounds: steps sum to %d, checksum %d\n", count, rounds, sum, check)
}
