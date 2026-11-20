// LeetCode #1220 bench, Go mirror of the Kāra ★ arm: five running counts,
// the strings of the length so far that end in each vowel, for every n from
// 1 to 8000; checksum of the answers.
package main

import "fmt"

func countVowelPermutation(n int64) int64 {
	const modulus = 1000000007
	a, e, i, o, u := int64(1), int64(1), int64(1), int64(1), int64(1)
	for k := int64(1); k < n; k++ {
		a, e, i, o, u = (e+i+u)%modulus, (a+i)%modulus, (e+o)%modulus, i, (i+o)%modulus
	}
	return (a + e + i + o + u) % modulus
}

func main() {
	var check int64
	for n := int64(1); n <= 8000; n++ {
		check = (check*131 + countVowelPermutation(n)) % 1000000007
	}
	fmt.Printf("every n from 1 to 8000: checksum %d\n", check)
}
