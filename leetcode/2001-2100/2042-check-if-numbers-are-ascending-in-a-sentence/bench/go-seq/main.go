// LeetCode #2042: Check if Numbers Are Ascending in a Sentence -- the ★ arm
// in Go, the same algorithm and workload as ascending.kara: the sentence
// split at its spaces, each token that parses compared with the last.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func areNumbersAscending(s string) bool {
	var last int64
	for _, token := range strings.Split(s, " ") {
		if n, err := strconv.ParseInt(token, 10, 64); err == nil {
			if n <= last {
				return false
			}
			last = n
		}
	}
	return true
}

var seed int64 = 2042

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func sentence() string {
	words := 1 + nextRandom()%30
	climb := nextRandom()%20 + 1
	drift := nextRandom() % 4
	last := nextRandom()%10 + 1
	var tokens []string
	numbers := 0
	length := 0
	for t := int64(0); t < words+2; t++ {
		var token string
		if t >= words || nextRandom()%3 == 0 {
			last = last + nextRandom()%(climb+drift+1) - drift
			if last < 1 {
				last = 1
			}
			if last > 99 {
				last = 99
			}
			numbers++
			token = strconv.FormatInt(last, 10)
		} else {
			n := nextRandom()%6 + 1
			b := make([]byte, n)
			for c := range b {
				b[c] = "abcxyz"[nextRandom()%6]
			}
			token = string(b)
		}
		if length+len(token)+1 > 200 && numbers >= 2 {
			break
		}
		length += len(token) + 1
		tokens = append(tokens, token)
	}
	return strings.Join(tokens, " ")
}

func main() {
	sentences := make([]string, 1000)
	for i := range sentences {
		sentences[i] = sentence()
	}
	var calls, ascending, check int64
	for round := int64(0); round < 1000; round++ {
		for i := range sentences {
			answer := areNumbersAscending(strings.Clone(sentences[i]))
			calls++
			if answer {
				ascending++
				check = (check*31 + round + int64(i)) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d ascending, checksum %d\n", calls, ascending, check)
}
