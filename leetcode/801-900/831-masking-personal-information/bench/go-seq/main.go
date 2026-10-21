// Benchmark for #831: Masking Personal Information -- the ★ arm (by the rules).
//
// Mirrors mask_pii.kara: an email keeps its name's first and last letter,
// lowered, around five `*`, and its domain lowered; a phone number shows
// its last four digits and masks the country code, the digits before the
// last ten.
package main

import (
	"fmt"
	"strings"
)

func maskPII(s string) string {
	if at := strings.IndexByte(s, '@'); at >= 0 {
		lower := strings.ToLower(s)
		return lower[0:1] + "*****" + lower[at-1:]
	}
	var digits []byte
	for i := 0; i < len(s); i++ {
		if s[i] >= '0' && s[i] <= '9' {
			digits = append(digits, s[i])
		}
	}
	n := len(digits)
	local := "***-***-" + string(digits[n-4:])
	if n == 10 {
		return local
	}
	return "+" + strings.Repeat("*", n-10) + "-" + local
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(seed *int64) byte {
	r := nextRandom(seed) % 52
	if r < 26 {
		return byte('a' + r)
	}
	return byte('A' + r - 26)
}

func main() {
	const count, rounds = int64(64), int64(12000000)
	separators := []byte{'+', '-', '(', ')', ' '}
	seed := int64(831)
	strs := make([]string, 0, count)
	for g := int64(0); g < count; g++ {
		var sb strings.Builder
		if g%2 == 0 {
			for i, m := int64(0), 2+nextRandom(&seed)%19; i < m; i++ {
				sb.WriteByte(letter(&seed))
			}
			sb.WriteByte('@')
			for i, m := int64(0), 1+nextRandom(&seed)%8; i < m; i++ {
				sb.WriteByte(letter(&seed))
			}
			sb.WriteByte('.')
			for i, m := int64(0), 1+nextRandom(&seed)%8; i < m; i++ {
				sb.WriteByte(letter(&seed))
			}
		} else {
			for i, m := int64(0), 10+nextRandom(&seed)%4; i < m; i++ {
				if nextRandom(&seed)%3 == 0 {
					sb.WriteByte(separators[nextRandom(&seed)%5])
				}
				sb.WriteByte(byte('0' + nextRandom(&seed)%10))
			}
		}
		strs = append(strs, sb.String())
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		m := maskPII(strs[round%count])
		total += int64(len(m))
		checksum = (checksum*131 + int64(m[len(m)-1])) % 1000000007
	}
	fmt.Printf("%d rounds of %d strings: %d characters, checksum %d\n", rounds, count, total, checksum)
}
