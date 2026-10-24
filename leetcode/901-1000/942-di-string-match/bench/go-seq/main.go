// Benchmark: LeetCode #942 DI String Match -- the ★ arm, the smallest
// and largest left, on 20 strings of 100000 letters, LeetCode's longest,
// in 50 rounds. Mirrors di_string_match.kara, .c, .rs and .py.
package main

import "fmt"

func diStringMatch(s string) []int64 {
	n := int64(len(s))
	lo, hi := int64(0), n
	perm := make([]int64, 0)
	for i := 0; i < len(s); i++ {
		if s[i] == 'I' {
			perm = append(perm, lo)
			lo++
		} else {
			perm = append(perm, hi)
			hi--
		}
	}
	return append(perm, lo)
}

var seed int64 = 942

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, n := 50, 20, 100000
	strings := make([]string, 0, count)
	for w := 0; w < count; w++ {
		odds := 1 + nextRandom()%15
		b := make([]byte, n)
		for i := range b {
			if nextRandom()%16 < odds {
				b[i] = 'I'
			} else {
				b[i] = 'D'
			}
		}
		strings = append(strings, string(b))
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			perm := diStringMatch(strings[(r+i)%count])
			check = (check*1000003 + perm[0]*3 + perm[n/2]*5 + perm[n]*7) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d strings of %d letters: checksum %d\n", rounds, count, n, check)
}
