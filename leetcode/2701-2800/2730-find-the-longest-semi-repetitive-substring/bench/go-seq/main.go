// LeetCode #2730: Find the Longest Semi-Repetitive Substring -- the bench
// (semi.kara in Go): a sliding window over the bytes holding at most one
// adjacent equal pair.
package main

import "fmt"

func longestSemiRepetitiveSubstring(s string) int64 {
	left, pairs := 0, 0
	best := int64(1)
	for right := 1; right < len(s); right++ {
		if s[right] == s[right-1] {
			pairs++
		}
		for pairs > 1 {
			if s[left] == s[left+1] {
				pairs--
			}
			left++
		}
		if int64(right-left+1) > best {
			best = int64(right - left + 1)
		}
	}
	return best
}

var seed int64 = 2730

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 200000, 20
	strings := make([]string, 0, count)
	for k := 0; k < count; k++ {
		digits := nextRandom()%9 + 2
		b := make([]byte, 50)
		for i := range b {
			b[i] = byte('0' + nextRandom()%digits)
		}
		strings = append(strings, string(b))
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			length := longestSemiRepetitiveSubstring(s)
			sum += length
			check = (check*31 + length + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d strings of 50 digits, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}
