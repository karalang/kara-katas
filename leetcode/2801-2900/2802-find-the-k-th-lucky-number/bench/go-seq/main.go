// LeetCode #2802: Find The K-th Lucky Number -- the bench in Go: the ★
// arm over 200000 k up to 10^9, all drawn first, then each answered 10
// times.
package main

import (
	"fmt"
	"strings"
)

func kthLuckyNumber(k int64) string {
	n := k + 1
	top := int64(1)
	for top*2 <= n {
		top *= 2
	}
	var lucky strings.Builder
	for bit := top / 2; bit > 0; bit /= 2 {
		if n&bit == 0 {
			lucky.WriteString("4")
		} else {
			lucky.WriteString("7")
		}
	}
	return lucky.String()
}

var seed int64 = 2802

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func digest(s string) int64 {
	var h int64
	for i := 0; i < len(s); i++ {
		h = (h*131 + int64(s[i])) % 1000000007
	}
	return h
}

func main() {
	count := 200000
	rounds := 10
	ks := make([]int64, count)
	for i := range ks {
		ks[i] = wide()%1000000000 + 1
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, k := range ks {
			s := kthLuckyNumber(k)
			total += int64(len(s))
			check = (check*31 + digest(s) + r) % 1000000007
		}
	}
	fmt.Printf("%d k up to 10^9, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, total, check)
}
