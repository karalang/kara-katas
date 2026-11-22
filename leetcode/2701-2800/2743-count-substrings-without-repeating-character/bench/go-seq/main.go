// LeetCode #2743: Count Substrings Without Repeating Character -- the
// bench (substrings.kara in Go): a window with each letter's last place.
package main

import "fmt"

func numberOfSpecialSubstrings(s string) int64 {
	var last [26]int64
	for i := range last {
		last[i] = -1
	}
	var start, count int64
	for i := 0; i < len(s); i++ {
		letter := s[i] - 'a'
		start = max(start, last[letter]+1)
		last[letter] = int64(i)
		count += int64(i) - start + 1
	}
	return count
}

var seed int64 = 2743

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, n, rounds = 20, 100000, 300
	words := make([]string, 0, count)
	for c := 0; c < count; c++ {
		k := nextRandom()%22 + 5
		bytes := make([]byte, 0, n)
		for i := 0; i < n; i++ {
			bytes = append(bytes, byte('a'+nextRandom()%k))
		}
		words = append(words, string(bytes))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, s := range words {
			found := numberOfSpecialSubstrings(s)
			sum += found
			check = (check*31 + found + r) % 1000000007
		}
	}
	fmt.Printf("%d words of %d letters, %d rounds: counts sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
