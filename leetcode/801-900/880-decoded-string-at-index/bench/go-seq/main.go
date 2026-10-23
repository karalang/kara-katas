// LeetCode #880 bench: Go mirror of decode_at_index.kara (the ★ arm, the
// tape's length, then back from the end) on the same 1,000,000 queries.
package main

import (
	"fmt"
	"strings"
)

func isDigit(b byte) bool {
	return b >= '0' && b <= '9'
}

func decodeAtIndex(s string, k int64) string {
	var size int64
	for i := 0; i < len(s); i++ {
		if isDigit(s[i]) {
			size *= int64(s[i] - '0')
		} else {
			size++
		}
	}
	for i := len(s) - 1; ; i-- {
		k %= size
		if k == 0 && !isDigit(s[i]) {
			return s[i : i+1]
		}
		if isDigit(s[i]) {
			size /= int64(s[i] - '0')
		} else {
			size--
		}
	}
}

var seed int64 = 880

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func upTo(limit int64) int64 {
	x := nextRandom()
	y := nextRandom()
	return (x*32768+y)%limit + 1
}

func encoded(length int64) (string, int64) {
	const letters = "abcdefghijklmnopqrstuvwxyz"
	const bound int64 = 1000000000000000000
	var sb strings.Builder
	var size int64
	for i := int64(0); i < length; i++ {
		d := nextRandom()%8 + 2
		if i > 0 && nextRandom()%3 == 0 && size*d <= bound {
			sb.WriteByte(byte('0' + d))
			size *= d
		} else if size < bound {
			sb.WriteByte(letters[nextRandom()%26])
			size++
		}
	}
	return sb.String(), size
}

func main() {
	strs := make([]string, 0, 1000)
	sizes := make([]int64, 0, 1000)
	for j := 0; j < 1000; j++ {
		length := nextRandom()%99 + 2
		s, size := encoded(length)
		strs = append(strs, s)
		sizes = append(sizes, size)
	}
	var total, check int64
	for q := 0; q < 1000000; q++ {
		j := q % 1000
		k := upTo(min(sizes[j], 1000000000))
		answer := int64(decodeAtIndex(strs[j], k)[0])
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("1000000 queries over 1000 strings: letters sum to %d, checksum %d\n", total, check)
}
