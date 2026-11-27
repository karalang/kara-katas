// LeetCode #1823: Find the Winner of the Circular Game -- the bench in Go:
// the ★ arm over 200000 calls on circles of 250 to 499 friends, each
// circle's size and count drawn from the checksum so far.
package main

import "fmt"

func findTheWinner(n, k int64) int64 {
	var winner int64
	for i := int64(2); i <= n; i++ {
		winner = (winner + k) % i
	}
	return winner + 1
}

func main() {
	var check int64
	for call := int64(0); call < 200000; call++ {
		n := 250 + (check+call)%250
		k := 1 + (check*7+call)%n
		check = (check*41 + findTheWinner(n, k)) % 1000000007
	}
	fmt.Printf("200000 calls: checksum %d\n", check)
}
