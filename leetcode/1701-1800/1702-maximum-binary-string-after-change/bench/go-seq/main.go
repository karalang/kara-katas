// LeetCode #1702: Maximum Binary String After Change -- the bench's Go
// mirror: the ★ arm on 50 random strings of 100000 digits, all drawn
// first, each answered 40 times.
package main

import (
	"fmt"
	"strings"
)

// one 0 left, at the first 0 plus the zeros less one
func maximumBinaryString(binary string) string {
	first, zeros := int64(-1), int64(0)
	for i := 0; i < len(binary); i++ {
		if binary[i] == '0' {
			if first < 0 {
				first = int64(i)
			}
			zeros++
		}
	}
	if zeros == 0 {
		return strings.Clone(binary)
	}
	var out strings.Builder
	out.Grow(len(binary))
	for i := int64(0); i < int64(len(binary)); i++ {
		if i == first+zeros-1 {
			out.WriteByte('0')
		} else {
			out.WriteByte('1')
		}
	}
	return out.String()
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1702

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50, 40, 100000
	strs := make([]string, 0, count)
	for c := 0; c < count; c++ {
		// each digit a 1 with a chance of its string's own, 0 to 10 in 10
		lean := nextRandom() % 11
		b := make([]byte, n)
		for i := range b {
			if nextRandom()%10 < lean {
				b[i] = '1'
			} else {
				b[i] = '0'
			}
		}
		strs = append(strs, string(b))
	}
	var ones, check int64
	for r := 0; r < rounds; r++ {
		for _, binary := range strs {
			answer := maximumBinaryString(binary)
			length := int64(len(answer))
			// the 0's place, or the length when none is left
			zero := int64(strings.IndexByte(answer, '0'))
			if zero < 0 {
				zero = length
			}
			if zero < length {
				ones += length - 1
			} else {
				ones += length
			}
			check = (check*31 + int64(answer[check%length]) + zero) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d digits, %d rounds: %d ones, checksum %d\n", count, n, rounds, ones, check)
}
