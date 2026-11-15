// LeetCode #2168: Unique Substrings With Equal Digit Frequency -- the
// benchmark's Go mirror of equal.kara.
package main

import "fmt"

func equalDigitFrequency(s string) int64 {
	n := len(s)
	found := map[string]struct{}{}
	for i := 0; i < n; i++ {
		var counts [10]int64
		var kinds, most int64
		for j := i; j < n; j++ {
			d := s[j] - '0'
			if counts[d] == 0 {
				kinds++
			}
			counts[d]++
			most = max(most, counts[d])
			if most*kinds == int64(j-i+1) {
				found[s[i:j+1]] = struct{}{}
			}
		}
	}
	return int64(len(found))
}

var seed int64 = 2168

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	digits := make([]byte, 1000)
	for i := range digits {
		digits[i] = byte('0' + nextRandom()%3)
	}
	var check int64
	for r := 0; r < 200; r++ {
		at := nextRandom() % 1000
		digits[at] = byte('0' + nextRandom()%3)
		check = (check*31 + equalDigitFrequency(string(digits))) % 1000000007
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
