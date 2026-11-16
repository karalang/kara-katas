// LeetCode #1177: Can Make Palindrome from Substring -- the ★ arm's bench
// in Go: the parity masks of every prefix, each query's odd letters counted
// with bits.OnesCount64 on two masks XORed. The same string, the same
// queries and the same 200 calls.
package main

import (
	"fmt"
	"math/bits"
)

func canMakePaliQueries(s string, queries [][]int64) []bool {
	masks := []int64{0}
	for i := 0; i < len(s); i++ {
		masks = append(masks, masks[len(masks)-1]^(1<<(s[i]-'a')))
	}
	answer := make([]bool, 0, len(queries))
	for _, q := range queries {
		answer = append(answer, int64(bits.OnesCount64(uint64(masks[q[1]+1]^masks[q[0]]))/2) <= q[2])
	}
	return answer
}

var seed int64 = 1177

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	b := make([]byte, 100000)
	for i := range b {
		b[i] = byte('a' + nextRandom()%26)
	}
	s := string(b)
	queries := make([][]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		x := nextRandom() % 100000
		y := nextRandom() % 100000
		queries = append(queries, []int64{min(x, y), max(x, y), nextRandom() % 14})
	}
	calls := 200
	var check int64
	for c := 0; c < calls; c++ {
		for _, a := range canMakePaliQueries(s, queries) {
			if a {
				check = (check*3 + 2) % 1000000007
			} else {
				check = (check*3 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: checksum %d\n", calls, check)
}
