// LeetCode #1044: Longest Duplicate Substring -- bench, Go mirror of
// longest_dup.kara (binary search on the length, rolling hash).
package main

import "fmt"

const base = 131
const modulus = 1_000_000_007

func longestDupSubstring(s string) string {
	b := []byte(s)
	low, high := 1, len(b)-1
	bestStart, bestLen := 0, 0
	for low <= high {
		length := (low + high) / 2
		if start, ok := repeatedWindow(b, length); ok {
			bestStart, bestLen = start, length
			low = length + 1
		} else {
			high = length - 1
		}
	}
	return s[bestStart : bestStart+bestLen]
}

func repeatedWindow(b []byte, length int) (int, bool) {
	n := len(b)
	lead := int64(1)
	for i := 1; i < length; i++ {
		lead = lead * base % modulus
	}
	hash := int64(0)
	for i := 0; i < length; i++ {
		hash = (hash*base + int64(b[i])) % modulus
	}
	seen := map[int64][]int{}
	found, have := 0, false
	for start := 0; ; start++ {
		earlier := false
		for _, j := range seen[hash] {
			if same(b, j, start, length) {
				earlier = true
				break
			}
		}
		if earlier {
			if !have || smaller(b, start, found, length) {
				found, have = start, true
			}
		} else {
			seen[hash] = append(seen[hash], start)
		}
		if start+length == n {
			break
		}
		hash = (hash - int64(b[start])*lead%modulus + modulus) % modulus
		hash = (hash*base + int64(b[start+length])) % modulus
	}
	return found, have
}

func same(b []byte, x, y, length int) bool {
	for k := 0; k < length; k++ {
		if b[x+k] != b[y+k] {
			return false
		}
	}
	return true
}

func smaller(b []byte, x, y, length int) bool {
	for k := 0; k < length; k++ {
		if b[x+k] != b[y+k] {
			return b[x+k] < b[y+k]
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count, n, rounds := 12, int64(30000), 2
	seed := int64(1044)
	ks := []int64{2, 4, 8, 26}
	strings := []string{}
	for c := 0; c < count; c++ {
		k := ks[c%4]
		letters := make([]byte, n)
		for i := range letters {
			letters[i] = byte('a' + nextRandom(&seed)%k)
		}
		if c%2 == 1 {
			from := nextRandom(&seed) % (n / 2)
			to := n/2 + nextRandom(&seed)%(n/2-n/8)
			for i := int64(0); i < n/8; i++ {
				letters[to+i] = letters[from+i]
			}
		}
		strings = append(strings, string(letters))
	}
	total, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			answer := longestDupSubstring(s)
			total += int64(len(answer))
			check = (check*131 + int64(len(answer)) + 1) % 1000000007
			for _, b := range []byte(answer) {
				check = (check*131 + int64(b)) % 1000000007
			}
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: total length %d, checksum %d\n", count, n, rounds, total, check)
}
