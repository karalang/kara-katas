// LeetCode #1216 bench, in Go: the ★ arm (the longest palindromic
// subsequence, one row at a time) on 48 strings of 1000 letters drawn
// once from 2, 4, 8 or 26 letters, each asked with k = 200, 400, 600 and
// 800; every answer folded into a checksum.
package main

import "fmt"

var seed int64 = 1216

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func isValidPalindrome(s string, k int64) bool {
	b := []byte(s)
	n := len(b)
	row := make([]int64, n)
	for i := n - 1; i >= 0; i-- {
		row[i] = 1
		var diagonal int64
		for j := i + 1; j < n; j++ {
			below := row[j]
			if b[i] == b[j] {
				row[j] = diagonal + 2
			} else if row[j-1] > row[j] {
				row[j] = row[j-1]
			}
			diagonal = below
		}
	}
	return int64(n)-row[n-1] <= k
}

func main() {
	alphabets := []int64{2, 4, 8, 26}
	texts := []string{}
	for t := 0; t < 48; t++ {
		letters := alphabets[t%4]
		buf := make([]byte, 1000)
		for i := range buf {
			buf[i] = byte('a' + nextRandom()%letters)
		}
		texts = append(texts, string(buf))
	}
	var check int64
	yes := 0
	for _, s := range texts {
		for _, k := range []int64{200, 400, 600, 800} {
			answer := isValidPalindrome(s, k)
			var a int64 = 1
			if answer {
				yes++
				a = 2
			}
			check = (check*131 + a + k) % 1000000007
		}
	}
	fmt.Printf("48 strings of 1000 letters, 4 budgets each: %d true, checksum %d\n", yes, check)
}
