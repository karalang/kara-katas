// LeetCode #2318: Number of Distinct Roll Sequences -- the bench, the ★
// arm in Go. The count of sequences ending in each pair of rolls, a 6 by
// 6 table rolled forward once per roll, each next roll coprime with the
// last and unlike the last two. O(216 n).
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func distinctSequences(n int64) int64 {
	const modulus = 1000000007
	if n == 1 {
		return 6
	}
	var ends [6][6]int64
	for a := int64(0); a < 6; a++ {
		for b := int64(0); b < 6; b++ {
			if a != b && gcd(a+1, b+1) == 1 {
				ends[a][b] = 1
			}
		}
	}
	for r := int64(2); r < n; r++ {
		var next [6][6]int64
		for a := int64(0); a < 6; a++ {
			for b := int64(0); b < 6; b++ {
				if ends[a][b] > 0 {
					for c := int64(0); c < 6; c++ {
						if c != a && c != b && gcd(b+1, c+1) == 1 {
							next[b][c] = (next[b][c] + ends[a][b]) % modulus
						}
					}
				}
			}
		}
		ends = next
	}
	var total int64
	for a := 0; a < 6; a++ {
		for b := 0; b < 6; b++ {
			total = (total + ends[a][b]) % modulus
		}
	}
	return total
}

func main() {
	var check int64
	for p := int64(0); p < 5; p++ {
		for n := int64(9981); n <= 10000; n++ {
			check = (check*31 + distinctSequences(n) + p) % 1000000007
		}
	}
	fmt.Printf("5 passes over 20 counts of rolls up to 10^4: checksum %d\n", check)
}
