// Benchmark workload for LeetCode #342 — Go mirror of power_of_four.kara.
package main

import "fmt"

const (
	LEN     = 500000
	PUNCHES = 100
	MODULUS = 1073741789
	I32_MIN = -2147483648
)

func isPowerOfFour(n int32) bool {
	return n > 0 && (n&(n-1)) == 0 && (n&0x55555555) != 0
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func twoTo(k int64) int32 {
	var p int32 = 1
	for i := int64(0); i < k; i++ {
		p *= 2
	}
	return p
}

func value(seed *int64) int32 {
	kind := next(seed) % 3
	if kind == 0 {
		return twoTo(2 * (next(seed) % 16))
	}
	if kind == 1 {
		r := next(seed) % 3
		if r == 0 {
			return twoTo(2*(next(seed)%15) + 1)
		}
		p := twoTo(2 * (next(seed) % 16))
		if r == 1 {
			return p + 1
		}
		return p - 1
	}
	hi := next(seed)*32768 + next(seed)
	return int32(hi*4 + next(seed)%4 + I32_MIN)
}

func main() {
	var seed int64 = 342
	a := make([]int32, 0)
	for i := 0; i < LEN; i++ {
		a = append(a, value(&seed))
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		pos := (next(&seed)*32768 + next(&seed)) % LEN
		a[pos] = value(&seed)
		var count, sum int64
		for _, x := range a {
			if isPowerOfFour(x) {
				count++
				sum += int64(x)
			}
		}
		sink = (sink*31 + count + sum%MODULUS) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
