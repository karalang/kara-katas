// LeetCode #2259: Remove Digit From Number to Maximize Result -- Go
// mirror of the ★ arm: the first occurrence followed by a larger digit,
// else the last occurrence. Same workload and checksum as remove.kara.
package main

import (
	"fmt"
	"strings"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func removeDigit(number string, digit byte) string {
	last := 0
	for i := 0; i < len(number); i++ {
		if number[i] == digit {
			last = i
			if i+1 < len(number) && number[i+1] > digit {
				break
			}
		}
	}
	return number[:last] + number[last+1:]
}

func main() {
	seed := int64(2259)
	var b strings.Builder
	for i := 0; i < 1000000; i++ {
		b.WriteByte(byte('1' + nextRandom(&seed)%9))
	}
	pool := b.String()
	check := int64(0)
	for t := 0; t < 1000000; t++ {
		hi := nextRandom(&seed)
		at := int((hi*32768 + nextRandom(&seed)) % (1000000 - 100))
		number := pool[at : at+100]
		answer := removeDigit(number, number[50])
		for k := 0; k < len(answer); k++ {
			check = (check*131 + int64(answer[k])) % 1000000007
		}
	}
	fmt.Printf("10^6 numbers of 100 digits: checksum %d\n", check)
}
