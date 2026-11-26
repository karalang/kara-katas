// LeetCode #1447 Simplified Fractions: the bench, a mirror of
// simplified_fractions.kara.
package main

import "fmt"

func simplifiedFractions(n int) []string {
	// every numerator below every denominator up to n, kept when the two
	// share no factor
	fractions := []string{}
	for d := 2; d <= n; d++ {
		for a := 1; a < d; a++ {
			if gcd(a, d) == 1 {
				fractions = append(fractions, fmt.Sprintf("%d/%d", a, d))
			}
		}
	}
	return fractions
}

func gcd(a, b int) int {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func main() {
	// every n from 1 to 100, 100 times over, each answer's letters counted
	// and folded to a checksum
	var check int64 = 0
	for r := 0; r < 100; r++ {
		for n := 1; n <= 100; n++ {
			var letters int64 = 0
			for _, f := range simplifiedFractions(n) {
				letters += int64(len(f))
			}
			check = (check*131 + letters) % 1000000007
		}
	}
	fmt.Printf("10000 answers: checksum %d\n", check)
}
