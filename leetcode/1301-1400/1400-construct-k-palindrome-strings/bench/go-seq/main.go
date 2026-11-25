// LeetCode #1400 bench -- Go: at least k letters, and at most k letters
// that appear an odd number of times, the letters counted in an array of
// 26.
package main

import "fmt"

func canConstruct(s string, k int32) bool {
	if int64(len(s)) < int64(k) {
		return false
	}
	count := make([]int64, 26)
	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
	}
	odd := int32(0)
	for _, c := range count {
		if c%2 == 1 {
			odd++
		}
	}
	return odd <= k
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n = 100000
	seed := int64(1400)
	letters := make([]byte, n)
	for i := range letters {
		letters[i] = byte(97 + nextRandom(&seed)%26)
	}
	check := int64(0)
	for r := 0; r < 3000; r++ {
		seed = (seed + check) % 2147483648
		at := nextRandom(&seed) % n
		letters[at] = byte(97 + nextRandom(&seed)%26)
		k := 1 + nextRandom(&seed)%30
		s := string(letters)
		got := int64(0)
		if canConstruct(s, int32(k)) {
			got = k
		}
		check = (check*131 + got + at) % 1000000007
	}
	fmt.Printf("3000 rounds over 10^5 letters: checksum %d\n", check)
}
