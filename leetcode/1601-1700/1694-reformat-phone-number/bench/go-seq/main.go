// LeetCode #1694: Reformat Phone Number -- the bench's Go mirror: the ★ arm
// on 100000 random numbers of 100 characters, all drawn first, each
// answered 40 times.
package main

import (
	"fmt"
	"strings"
)

func reformatNumber(number string) string {
	var digits strings.Builder
	for _, c := range number {
		if c >= '0' && c <= '9' {
			digits.WriteRune(c)
		}
	}
	d := digits.String()
	var blocks []string
	at := 0
	for len(d)-at > 4 {
		blocks = append(blocks, d[at:at+3])
		at += 3
	}
	if len(d)-at == 4 {
		blocks = append(blocks, d[at:at+2], d[at+2:])
	} else {
		blocks = append(blocks, d[at:])
	}
	return strings.Join(blocks, "-")
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1694

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, length = 100000, 40, 100
	const alphabet = "0123456789 -"
	numbers := make([]string, count)
	for c := range numbers {
		number := make([]byte, length)
		for i := range number {
			var pick int64
			if i < 2 {
				pick = nextRandom() % 10
			} else {
				pick = nextRandom() % 12
			}
			number[i] = alphabet[pick]
		}
		numbers[c] = string(number)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, number := range numbers {
			answer := reformatNumber(number)
			n := int64(len(answer))
			total += n
			check = (check*31 + n + int64(answer[n/2]) + int64(answer[n-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d numbers of %d characters, %d rounds: %d characters out, checksum %d\n", count, length, rounds, total, check)
}
