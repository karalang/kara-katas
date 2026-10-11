// Benchmark for #372 -- mirror of super_pow.kara.
package main

import "fmt"

const modulus = 1337

func powMod(base, exp int64) int64 {
	out := int64(1)
	for i := int64(0); i < exp; i++ {
		out = out * base % modulus
	}
	return out
}

func superPow(a int64, b []int64) int64 {
	base := a % modulus
	out := int64(1)
	for _, d := range b {
		out = powMod(out, 10) * powMod(base, d) % modulus
	}
	return out
}

func main() {
	var seed int64 = 372
	var checksum int64
	b := make([]int64, 2000)
	for r := 0; r < 500; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		a := 1 + (high*65536+seed/32768)%2147483647
		for k := 0; k < 2000; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			d := (seed / 65536) % 10
			if k == 0 && d == 0 {
				d = 1
			}
			b[k] = d
		}
		checksum = (checksum*1337 + superPow(a, b)) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
