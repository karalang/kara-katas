// LeetCode #1611: Minimum One Bit Operations to Make Integers Zero -- the
// bench in Go, mirroring one_bit.kara: n turned back from Gray code, the
// XOR of n and all its right shifts.
package main

import "fmt"

func minimumOneBitOperations(n int32) int32 {
	var k int32
	for n > 0 {
		k ^= n
		n >>= 1
	}
	return k
}

func main() {
	seed := int64(1611)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	numbers := make([]int32, 0, 10000000)
	for i := 0; i < 10000000; i++ {
		a := nextRandom()
		b := nextRandom()
		numbers = append(numbers, int32((a*32768+b)%1000000001))
	}
	var check, total int64
	for _, n := range numbers {
		ops := int64(minimumOneBitOperations(n))
		check = (check*31 + ops + 1) % 1000000007
		total += ops
	}
	fmt.Printf("10000000 numbers up to 10^9: total %d, checksum %d\n", total, check)
}
