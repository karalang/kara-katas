// LeetCode #2309: Greatest English Letter in Upper and Lower Case -- the
// bench, the ★ arm in Go. A mask of the lowercase letters and one of the
// uppercase; the highest bit of their & is the answer.
package main

import "fmt"

func greatestLetter(s string) string {
	var lower, upper int64
	for i := 0; i < len(s); i++ {
		b := s[i]
		if b >= 'a' {
			lower |= 1 << (b - 'a')
		} else {
			upper |= 1 << (b - 'A')
		}
	}
	both := lower & upper
	for i := 25; i >= 0; i-- {
		if (both>>i)&1 == 1 {
			return string(rune('A' + i))
		}
	}
	return ""
}

var seed int64 = 2309

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	strings := make([]string, 1000)
	for a := range strings {
		pool := nextRandom()%30 + 1
		from := make([]byte, pool)
		for i := range from {
			from[i] = letters[nextRandom()%52]
		}
		s := make([]byte, 1000)
		for i := range s {
			s[i] = from[nextRandom()%pool]
		}
		strings[a] = string(s)
	}
	var check int64
	for p := 0; p < 100; p++ {
		for _, s := range strings {
			letter := greatestLetter(s)
			var code int64
			if letter != "" {
				code = int64(letter[0])
			}
			check = (check*31 + code) % 1000000007
		}
	}
	fmt.Printf("100 passes over 1000 strings of 1000 letters: checksum %d\n", check)
}
