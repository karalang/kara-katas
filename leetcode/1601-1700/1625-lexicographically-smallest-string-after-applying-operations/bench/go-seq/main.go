// LeetCode #1625: Lexicographically Smallest String After Applying
// Operations -- the bench in Go, mirroring smallest.kara: every rotation
// by a multiple of gcd(b, n) with every count of additions, each string
// made and the least kept.
package main

import (
	"fmt"
	"strings"
)

func gcd(x, y int64) int64 {
	if y == 0 {
		return x
	}
	return gcd(y, x%y)
}

func findLexSmallestString(s string, a, b int32) string {
	n := int64(len(s))
	digits := make([]int64, n)
	for i := int64(0); i < n; i++ {
		digits[i] = int64(s[i] - '0')
	}
	step := gcd(int64(b), n)
	evenCounts := int64(1)
	if b%2 == 1 {
		evenCounts = 10
	}
	best := s
	for start := int64(0); start < n; start += step {
		for odd := int64(0); odd < 10; odd++ {
			for even := int64(0); even < evenCounts; even++ {
				var t strings.Builder
				for i := int64(0); i < n; i++ {
					count := even
					if i%2 == 1 {
						count = odd
					}
					t.WriteByte(byte('0' + (digits[(i+start)%n]+count*int64(a))%10))
				}
				if ts := t.String(); ts < best {
					best = ts
				}
			}
		}
	}
	return best
}

var seed int64 = 1625

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type kase struct {
	s    string
	a, b int32
}

func main() {
	cases := make([]kase, 0, 200)
	for k := 0; k < 200; k++ {
		var sb strings.Builder
		for i := 0; i < 100; i++ {
			sb.WriteByte(byte('0' + nextRandom()%10))
		}
		a := int32(nextRandom()%9 + 1)
		b := int32(nextRandom()%99 + 1)
		cases = append(cases, kase{sb.String(), a, b})
	}
	var check, zeros int64
	for _, c := range cases {
		got := findLexSmallestString(c.s, c.a, c.b)
		for i := 0; i < len(got); i++ {
			if got[i] == '0' {
				zeros++
			}
			check = (check*31 + int64(got[i]-'0') + 1) % 1000000007
		}
	}
	fmt.Printf("200 cases of 100 digits: %d zeros in the answers, checksum %d\n", zeros, check)
}
