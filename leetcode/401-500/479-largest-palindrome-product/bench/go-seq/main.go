// Benchmark for #479: Go mirror of the ★ arm (palindromes from the top);
// see ../largest_palindrome_product.kara.
package main

import "fmt"

func largestPalindrome(n int64) int64 {
	if n == 1 {
		return 9
	}
	var upper int64 = 1
	for i := int64(0); i < n; i++ {
		upper *= 10
	}
	lower := upper / 10
	upper--
	for half := upper; half >= lower; half-- {
		palindrome, rest := half, half
		for rest > 0 {
			palindrome = palindrome*10 + rest%10
			rest /= 10
		}
		for factor := upper; factor*factor >= palindrome; factor-- {
			if palindrome%factor == 0 && palindrome/factor >= lower {
				return palindrome % 1337
			}
		}
	}
	return -1
}

func main() {
	rounds := 10
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for n := int64(1); n <= 8; n++ {
			got := largestPalindrome(n)
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d rounds of n = 1 to 8: answers add up to %d, checksum %d\n", rounds, total, checksum)
}
