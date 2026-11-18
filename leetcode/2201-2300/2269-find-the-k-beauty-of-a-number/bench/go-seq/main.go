// LeetCode #2269: Find the K-Beauty of a Number -- the bench, the ★ arm.
package main

import (
	"fmt"
	"strconv"
)

func divisorSubstrings(num int64, k int) int64 {
	s := strconv.FormatInt(num, 10)
	var beauty int64
	for i := 0; i <= len(s)-k; i++ {
		part, _ := strconv.ParseInt(s[i:i+k], 10, 64)
		if part != 0 && num%part == 0 {
			beauty++
		}
	}
	return beauty
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2269

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for t := 0; t < 200000; t++ {
		hi := nextRandom()
		num := (hi*32768+nextRandom())%1000000000 + 1
		k := t%9 + 1
		if l := len(strconv.FormatInt(num, 10)); l < k {
			k = l
		}
		check = (check*31 + divisorSubstrings(num, k)) % 1000000007
	}
	fmt.Printf("200000 numbers: checksum %d\n", check)
}
