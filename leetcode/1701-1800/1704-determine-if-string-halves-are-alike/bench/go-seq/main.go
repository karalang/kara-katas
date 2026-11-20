// LeetCode #1704: Determine if String Halves Are Alike -- the bench's Go
// mirror: the ★ arm on 1000 random strings of 1000 letters, all drawn
// first, each answered 400 times.
package main

import "fmt"

// one pass: a vowel in the first half counted up and in the second down
func halvesAreAlike(s string) bool {
	half := len(s) / 2
	balance := 0
	for i := 0; i < len(s); i++ {
		switch s[i] {
		case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U':
			if i < half {
				balance++
			} else {
				balance--
			}
		}
	}
	return balance == 0
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1704

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 1000, 400, 1000
	vowels := "aeiouAEIOU"
	consonants := "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
	strs := make([]string, 0, count)
	for c := 0; c < count; c++ {
		// each letter a vowel with a chance of its string's own, 0 to 10 in 10
		lean := nextRandom() % 11
		b := make([]byte, 0, n)
		for i := 0; i < n; i++ {
			if nextRandom()%10 < lean {
				b = append(b, vowels[nextRandom()%int64(len(vowels))])
			} else {
				b = append(b, consonants[nextRandom()%int64(len(consonants))])
			}
		}
		strs = append(strs, string(b))
	}
	var alike, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range strs {
			answer := halvesAreAlike(s)
			v := int64(2)
			if answer {
				alike++
				v = 1
			}
			check = (check*31 + v + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: %d alike, checksum %d\n", count, n, rounds, alike, check)
}
