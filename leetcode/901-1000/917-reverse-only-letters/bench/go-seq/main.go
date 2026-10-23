// LeetCode #917: Reverse Only Letters -- bench: Go mirror of the two
// pointers swapping letters in reverse_only_letters.kara.
package main

import (
	"fmt"
	"strings"
)

func isLetter(b byte) bool {
	return (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z')
}

func reverseOnlyLetters(s string) string {
	bytes := []byte(s)
	i, j := 0, len(bytes)
	for i < j {
		if !isLetter(bytes[i]) {
			i++
		} else if !isLetter(bytes[j-1]) {
			j--
		} else {
			bytes[i], bytes[j-1] = bytes[j-1], bytes[i]
			i++
			j--
		}
	}
	var out strings.Builder
	for _, b := range bytes {
		out.WriteByte(b)
	}
	return out.String()
}

var seed int64 = 917

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomString(letters int64) string {
	s := make([]byte, 100)
	for k := range s {
		if nextRandom()%100 < letters {
			c := nextRandom() % 52
			if c < 26 {
				s[k] = byte(97 + c)
			} else {
				s[k] = byte(65 + c - 26)
			}
		} else {
			var b int64 = 34
			for b == 34 || b == 92 {
				b = 33 + nextRandom()%90
			}
			s[k] = byte(b)
		}
	}
	return string(s)
}

func main() {
	rounds := 1000
	n := 1000
	pool := make([]string, n)
	for c := range pool {
		pool[c] = randomString(int64(c % 101))
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for _, s := range pool {
			out := reverseOnlyLetters(s)
			check = (check*1000003 + int64(out[0])*256 + int64(out[len(out)-1])) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d strings of 100: checksum %d\n", rounds, n, check)
}
