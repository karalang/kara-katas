// LeetCode #2351: First Letter to Appear Twice -- the bench, the ★ arm in
// Go: a table of 26 marks, one per letter, the first letter already marked
// is the answer.
package main

import "fmt"

func repeatedCharacter(s string) byte {
	var seen [26]bool
	for i := 0; i < len(s); i++ {
		c := s[i]
		if seen[c-'a'] {
			return c
		}
		seen[c-'a'] = true
	}
	return ' '
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// string t is the first 2 to 26 letters of the alphabet shuffled, then
	// one of them again
	seed := int64(2351)
	strings := make([]string, 0, 100000)
	for t := 0; t < 100000; t++ {
		k := 2 + nextRandom(&seed)%25
		letters := make([]byte, k, k+1)
		for i := int64(0); i < k; i++ {
			letters[i] = byte(97 + i)
		}
		for i := k - 1; i >= 1; i-- {
			j := nextRandom(&seed) % (i + 1)
			letters[i], letters[j] = letters[j], letters[i]
		}
		letters = append(letters, letters[nextRandom(&seed)%k])
		strings = append(strings, string(letters))
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for _, s := range strings {
			check = (check*31 + int64(repeatedCharacter(s)) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10^5 strings: checksum %d\n", check)
}
