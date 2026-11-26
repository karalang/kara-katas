// LeetCode #1780: Check if Number is a Sum of Powers of Three -- the bench in
// Go, mirroring check_powers_of_three.kara: base-3 digits read off from the
// lowest, on every n from 1 to 10^7, five rounds over.
package main

import "fmt"

func checkPowersOfThree(n int32) bool {
	rest := n
	for rest > 0 {
		if rest%3 == 2 {
			return false
		}
		rest /= 3
	}
	return true
}

func main() {
	var count, check int64
	for round := int64(0); round < 5; round++ {
		for n := int32(1); n < 10000001; n++ {
			if checkPowersOfThree(n) {
				count++
				check = (check*31 + int64(n) + round) % 1000000007
			}
		}
	}
	fmt.Printf("5 rounds of 1 to 10000000: %d sums, checksum %d\n", count, check)
}
