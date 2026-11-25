// LeetCode #1392 bench, Go mirror of the ★ arm.
package main

import "fmt"

func longestPrefix(s string) string {
	n := len(s)
	border := make([]int, n)
	k := 0
	for i := 1; i < n; i++ {
		for k > 0 && s[i] != s[k] {
			k = border[k-1]
		}
		if s[i] == s[k] {
			k++
		}
		border[i] = k
	}
	return s[:border[n-1]]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n = 100000
	block := "abacaba"
	letters := make([]byte, n)
	for i := range letters {
		letters[i] = block[i%7]
	}
	var seed int64 = 1392
	var check int64
	for round := 0; round < 2000; round++ {
		seed = (seed + check) % 2147483648
		at := nextRandom(&seed) % n
		was := letters[at]
		letters[at] = byte(97 + nextRandom(&seed)%3)
		s := string(letters)
		got := longestPrefix(s)
		letters[at] = was
		check = (check*131 + int64(len(got))*7 + at) % 1000000007
	}
	fmt.Printf("2000 rounds over 10^5 letters: checksum %d\n", check)
}
