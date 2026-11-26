package main

import (
	"fmt"
	"math"
)

func maxScore(s string) int32 {
	digits := []byte(s)
	var ones int32
	for _, d := range digits {
		if d == '1' {
			ones++
		}
	}
	var lead int32
	best := int32(math.MinInt32)
	for _, d := range digits[:len(digits)-1] {
		if d == '0' {
			lead++
		} else {
			lead--
		}
		if lead > best {
			best = lead
		}
	}
	return ones + best
}

func main() {
	var seed int64 = 1422
	pool := make([]byte, 1000000)
	for i := range pool {
		seed = (seed*1103515245 + 12345) % 2147483648
		if seed/65536%2 == 0 {
			pool[i] = '0'
		} else {
			pool[i] = '1'
		}
	}
	text := string(pool)
	var check int64
	for w := 0; w < 1000000; w++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		start := seed / 65536 % 999501
		check = (check*131 + int64(maxScore(text[start:start+500]))) % 1000000007
	}
	fmt.Printf("10^6 windows of 500 digits: checksum %d\n", check)
}
