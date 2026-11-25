// LeetCode #1374 bench -- Go: the ★ arm: n a's when n is odd, and n - 1
// a's and a b when it is even.
package main

import (
	"fmt"
	"strings"
)

func generateTheString(n int) string {
	if n%2 == 1 {
		return strings.Repeat("a", n)
	}
	return strings.Repeat("a", n-1) + "b"
}

func main() {
	// 10^7 rounds, each making the string for an n from 1 to 500, the
	// constraints' range, drawn from the checksum so far, and reading its
	// length and one letter at a place drawn the same way
	var check int64
	for r := int64(0); r < 10000000; r++ {
		s := generateTheString(int(1 + check%500))
		n := int64(len(s))
		b := int64(s[(check/500)%n])
		check = (check*31 + n + b + r) % 1000000007
	}
	fmt.Printf("10000000 rounds: checksum %d\n", check)
}
