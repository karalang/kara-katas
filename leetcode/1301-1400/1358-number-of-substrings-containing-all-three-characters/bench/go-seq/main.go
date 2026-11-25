// LeetCode #1358 bench -- Go: where each of a, b and c was last seen; a
// substring ending at i holds all three when it starts at or before the
// earliest of those places.
package main

import "fmt"

func numberOfSubstrings(s []byte) int64 {
	last := [3]int64{-1, -1, -1}
	var count int64
	for i, b := range s {
		last[b-'a'] = int64(i)
		count += min(last[0], last[1], last[2]) + 1
	}
	return count
}

var seed int64 = 1358

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 20 strings of 5 * 10^4 letters, the constraints' most, c drawn one
	// time in 1000 and a and b evenly, built once; then 1000 rounds, each
	// setting one letter of one string, both drawn from the checksum so
	// far, and counting that string's substrings
	texts := make([][]byte, 20)
	for k := range texts {
		texts[k] = make([]byte, 50000)
		for i := range texts[k] {
			r := nextRandom() % 1000
			switch {
			case r == 0:
				texts[k][i] = 'c'
			case r%2 == 0:
				texts[k][i] = 'a'
			default:
				texts[k][i] = 'b'
			}
		}
	}
	var check int64
	for r := int64(0); r < 1000; r++ {
		k := check % 20
		texts[k][(check/20)%50000] = byte(97 + (check/7)%3)
		check = (check*31 + numberOfSubstrings(texts[k]) + r) % 1000000007
	}
	fmt.Printf("1000 rounds over 20 strings of 5 * 10^4 letters: checksum %d\n", check)
}
