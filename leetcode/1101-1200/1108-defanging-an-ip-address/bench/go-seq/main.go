// LeetCode #1108: Defanging an IP Address -- the bench in Go: the ★ arm
// (one pass, each period written as `[.]`) over 1024 random addresses,
// each round replacing one address with a new one and defanging every
// address again.
package main

import (
	"fmt"
	"strings"
)

func defangIPAddr(address string) string {
	var out strings.Builder
	out.Grow(len(address) + 6)
	for _, c := range address {
		if c == '.' {
			out.WriteString("[.]")
		} else {
			out.WriteRune(c)
		}
	}
	return out.String()
}

var seed int64 = 1108

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomAddress() string {
	a := nextRandom() % 256
	b := nextRandom() % 256
	c := nextRandom() % 256
	d := nextRandom() % 256
	return fmt.Sprintf("%d.%d.%d.%d", a, b, c, d)
}

func main() {
	addresses := make([]string, 1024)
	for i := range addresses {
		addresses[i] = randomAddress()
	}
	length := 0
	var check, calls int64
	for round := 0; round < 10000; round++ {
		addresses[(round*7919)%1024] = randomAddress()
		for _, a := range addresses {
			d := defangIPAddr(a)
			length += len(d)
			if calls%64 == 0 {
				for _, c := range d {
					check = (check*31 + int64(c)) % 1000000007
				}
			}
			calls++
		}
	}
	fmt.Printf("10000 rounds over 1024 addresses: %d calls, %d characters, checksum %d\n", calls, length, check)
}
