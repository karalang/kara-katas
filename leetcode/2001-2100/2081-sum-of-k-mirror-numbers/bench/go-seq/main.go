// LeetCode #2081: Sum of k-Mirror Numbers -- Go mirror of the ★ arm's
// benchmark (kmirror.kara): every base from 2 to 9 asked for every `n`
// from 1 to 32, each search started afresh: 256 searches.
package main

import "fmt"

func isMirror(x, k int64) bool {
	digits := []int64{}
	for y := x; y > 0; y /= k {
		digits = append(digits, y%k)
	}
	m := len(digits)
	for i := 0; i < m/2; i++ {
		if digits[i] != digits[m-1-i] {
			return false
		}
	}
	return true
}

func kMirror(k, n int64) int64 {
	var sum, found int64
	for length := int64(1); ; length++ {
		half := (length + 1) / 2
		start := int64(1)
		for i := int64(1); i < half; i++ {
			start *= 10
		}
		for h := start; h < start*10; h++ {
			p := h
			rest := h
			if length%2 == 1 {
				rest = h / 10
			}
			for rest > 0 {
				p = p*10 + rest%10
				rest /= 10
			}
			if isMirror(p, k) {
				sum += p
				found++
				if found == n {
					return sum
				}
			}
		}
	}
}

func main() {
	var total, check int64
	for k := int64(2); k < 10; k++ {
		for n := int64(1); n < 33; n++ {
			a := kMirror(k, n)
			total += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("256 answers: sum %d, checksum %d\n", total, check)
}
