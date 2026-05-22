// LeetCode #91 — Go seq bench peer for decode_ways.kara. Same algorithm,
// same workload, same sink as the Kara/Rust/C mirrors.

package main

import "fmt"

const (
	l       = 80
	nIters  = 10000000
	modulus = int64(1_000_000_007)
)

func decodeWays(bytes []byte) int64 {
	n := len(bytes)
	if n == 0 {
		return 0
	}
	const zero byte = '0'
	if bytes[0] == zero {
		return 0
	}

	var prev2 int64 = 1
	var prev1 int64 = 1

	for i := 1; i < n; i++ {
		d1 := int32(bytes[i]) - int32(zero)
		d0 := int32(bytes[i-1]) - int32(zero)
		two := d0*10 + d1

		var cur int64 = 0
		if d1 >= 1 && d1 <= 9 {
			cur += prev1
		}
		if two >= 10 && two <= 26 {
			cur += prev2
		}

		prev2 = prev1
		prev1 = cur
	}

	return prev1
}

func main() {
	const zero byte = '0'
	buf := make([]byte, l)
	for j := int64(0); j < l; j++ {
		d := ((j * 3) % 9) + 1
		buf[j] = zero + byte(d)
	}

	var sum int64 = 0
	for k := int64(0); k < nIters; k++ {
		pos := k % l
		d := ((k * 11) % 9) + 1
		buf[pos] = zero + byte(d)
		sum = (sum + decodeWays(buf)) % modulus
	}
	fmt.Println(sum)
}
