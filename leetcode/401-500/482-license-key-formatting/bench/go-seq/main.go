// Benchmark for #482: Go mirror of the ★ arm (back to front); see
// ../license_key_formatting.kara.
package main

import (
	"fmt"
	"strings"
)

func licenseKeyFormatting(s string, k int64) string {
	runes := []rune(s)
	backwards := []rune{}
	var inGroup int64
	for i := len(runes) - 1; i >= 0; i-- {
		c := runes[i]
		if c == '-' {
			continue
		}
		if inGroup == k {
			backwards = append(backwards, '-')
			inGroup = 0
		}
		if c >= 'a' && c <= 'z' {
			c = c - 'a' + 'A'
		}
		backwards = append(backwards, c)
		inGroup++
	}
	for i, j := 0, len(backwards)-1; i < j; i, j = i+1, j-1 {
		backwards[i], backwards[j] = backwards[j], backwards[i]
	}
	var key strings.Builder
	for _, c := range backwards {
		key.WriteRune(c)
	}
	return key.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	alphabet := []rune("abcxyzABCXYZ0189")
	var seed int64 = 482
	var sb strings.Builder
	for i := 0; i < 100000; i++ {
		if nextRandom(&seed)%4 == 0 {
			sb.WriteRune('-')
		} else {
			sb.WriteRune(alphabet[nextRandom(&seed)%int64(len(alphabet))])
		}
	}
	s := sb.String()
	var total, checksum int64
	for k := int64(1); k <= 500; k++ {
		key := licenseKeyFormatting(s, k)
		n := int64(len(key))
		total += n
		checksum = (checksum*31 + n*7 + int64(key[n/2]) + int64(key[k])) % 1000000007
	}
	fmt.Printf("k = 1 to 500 on 100000 characters: keys add up to %d characters, checksum %d\n", total, checksum)
}
