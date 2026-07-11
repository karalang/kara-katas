// Benchmark workload — Restore IP Addresses (LeetCode #93).
// Go mirror of ../restore_ip.kara. Folds segment values of every valid quadruple
// through a rolling polynomial hash; digits computed inline. Input length varies per
// iteration (n = 4 + iter%9) so the fixed-shape enumeration can't be vectorized away.
// K=6,500,000.
package main

import "fmt"

func digit(pos, iter int64) int64 {
	return (pos*7 + iter) % 10
}

func segVal(start, length, iter int64) int64 {
	if length < 1 || length > 3 {
		return -1
	}
	if length > 1 && digit(start, iter) == 0 {
		return -1
	}
	var v int64 = 0
	for i := int64(0); i < length; i++ {
		v = v*10 + digit(start+i, iter)
	}
	if v > 255 {
		return -1
	}
	return v
}

func restoreFold(n, iter, seed int64) int64 {
	acc := seed
	for a := int64(1); a <= 3 && a < n; a++ {
		v0 := segVal(0, a, iter)
		if v0 < 0 {
			continue
		}
		for b := a + 1; b <= a+3 && b < n; b++ {
			v1 := segVal(a, b-a, iter)
			if v1 < 0 {
				continue
			}
			for c := b + 1; c <= b+3 && c < n; c++ {
				v2 := segVal(b, c-b, iter)
				v3 := segVal(c, n-c, iter)
				if v2 >= 0 && v3 >= 0 {
					acc = (acc*131 + v0*1000000 + v1*10000 + v2*100 + v3 + 1) % 1000000007
				}
			}
		}
	}
	return acc
}

func main() {
	const total = 6500000
	const modulus = 1000000007
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		n := 4 + (iter % 9) // 4..12 — data-dependent length
		sum = (sum*131 + restoreFold(n, iter, iter)) % modulus
	}
	fmt.Println(sum)
}
