// Benchmark workload for LeetCode #326 — Go mirror of power_of_three.kara.
package main

import "fmt"

const LEN = 300000
const PUNCHES = 40
const MODULUS = 1073741789
const I32_MIN = -2147483648

func isPowerOfThree(n int64) bool {
	if n <= 0 {
		return false
	}
	m := n
	for m%3 == 0 {
		m /= 3
	}
	return m == 1
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func power(k int64) int64 {
	p := int64(1)
	for i := int64(0); i < k; i++ {
		p *= 3
	}
	return p
}

func value(seed *int64) int64 {
	kind := next(seed) % 3
	if kind == 0 {
		return power(next(seed) % 20)
	}
	if kind == 1 {
		p := power(next(seed) % 20)
		if next(seed)%2 == 0 {
			return p + 1
		}
		return p - 1
	}
	hi := next(seed)*32768 + next(seed)
	return hi*4 + next(seed)%4 + I32_MIN
}

func main() {
	seed := int64(326)
	a := make([]int64, 0, LEN)
	for i := 0; i < LEN; i++ {
		a = append(a, value(&seed))
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		pos := (next(&seed)*32768 + next(&seed)) % LEN
		a[pos] = value(&seed)
		var count, sum int64
		for _, x := range a {
			if isPowerOfThree(x) {
				count++
				sum += x
			}
		}
		sink = (sink*31 + count + sum%MODULUS) % MODULUS
	}
	fmt.Printf("sink %d\n", sink)
}
