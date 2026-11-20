// LeetCode #1717: Maximum Score From Removing Substrings -- the Go mirror
// of the bench (score.kara): the pair worth more removed first with a
// stack, then the other pair from what is left, on 20 random strings of
// 100000 letters, each answered 100 times.
package main

import (
	"fmt"
	"strings"
)

func remove(chars []rune, first, second rune, points int32) ([]rune, int32) {
	kept := []rune{}
	var gained int32
	for _, c := range chars {
		if c == second && len(kept) > 0 && kept[len(kept)-1] == first {
			kept = kept[:len(kept)-1]
			gained += points
		} else {
			kept = append(kept, c)
		}
	}
	return kept, gained
}

func maximumGain(s string, x, y int32) int32 {
	chars := []rune(s)
	first, second, more, less := 'b', 'a', y, x
	if x >= y {
		first, second, more, less = 'a', 'b', x, y
	}
	rest, a := remove(chars, first, second, more)
	_, b := remove(rest, second, first, less)
	return a + b
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 20
	var rounds int64 = 100
	n := 100000
	var seed int64 = 1717
	strs := make([]string, count)
	xs := make([]int32, count)
	ys := make([]int32, count)
	for p := 0; p < count; p++ {
		var sb strings.Builder
		for i := 0; i < n; i++ {
			r := nextRandom(&seed) % 200
			if r < 2 {
				sb.WriteByte('c')
			} else if r%2 == 0 {
				sb.WriteByte('a')
			} else {
				sb.WriteByte('b')
			}
		}
		strs[p] = sb.String()
		xs[p] = int32(nextRandom(&seed)%10000 + 1)
		ys[p] = int32(nextRandom(&seed)%10000 + 1)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := int64(maximumGain(strs[p], xs[p], ys[p]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
