// LeetCode #2429: Minimize XOR -- the bench, the ★ arm: num1's set bits
// taken from the top while bits are left to place, the rest laid in its
// clear bits from the bottom.
package main

import (
	"fmt"
	"math/bits"
)

func minimizeXor(num1, num2 int64) int64 {
	left := int64(bits.OnesCount64(uint64(num2)))
	var x int64
	for bit := 30; bit >= 0; bit-- {
		if left > 0 && (num1>>bit)&1 == 1 {
			x |= 1 << bit
			left--
		}
	}
	for bit := 0; bit < 31; bit++ {
		if left > 0 && (x>>bit)&1 == 0 {
			x |= 1 << bit
			left--
		}
	}
	return x
}

var seed int64 = 2429

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var firsts, seconds []int64
	for i := 0; i < 100000; i++ {
		a := nextRandom()
		firsts = append(firsts, 1+(a*32768+nextRandom())%1000000000)
		b := nextRandom()
		seconds = append(seconds, 1+(b*32768+nextRandom())%1000000000)
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for i := range firsts {
			check = (check*31 + minimizeXor(firsts[i], seconds[i]^(p+1)) + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 10^5 pairs: checksum %d\n", check)
}
