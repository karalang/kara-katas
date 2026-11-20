// LeetCode #1247 bench, in Go: the ★ arm (the places that differ counted
// by kind over the two strings side by side) on 2000 random pairs of 1000
// letters built once, each with its own mix of x and y, each asked 20
// times; every answer folded into a checksum.
package main

import (
	"fmt"
	"strings"
)

func minimumSwap(s1, s2 string) int64 {
	var xOverY, yOverX int64
	for i := 0; i < len(s1) && i < len(s2); i++ {
		if s1[i] == 'x' && s2[i] == 'y' {
			xOverY++
		} else if s1[i] == 'y' && s2[i] == 'x' {
			yOverX++
		}
	}
	if (xOverY+yOverX)%2 == 1 {
		return -1
	}
	return xOverY/2 + yOverX/2 + 2*(xOverY%2)
}

var seed int64 = 1247

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomXY(n int, percent int64) string {
	var b strings.Builder
	for i := 0; i < n; i++ {
		if nextRandom()%100 < percent {
			b.WriteByte('x')
		} else {
			b.WriteByte('y')
		}
	}
	return b.String()
}

func main() {
	type pair struct{ s1, s2 string }
	pairs := make([]pair, 0, 2000)
	for p := 0; p < 2000; p++ {
		p1 := nextRandom() % 101
		p2 := nextRandom() % 101
		s1 := randomXY(1000, p1)
		s2 := randomXY(1000, p2)
		pairs = append(pairs, pair{s1, s2})
	}
	var check int64
	for r := 0; r < 20; r++ {
		for _, p := range pairs {
			check = (check*131 + minimumSwap(p.s1, p.s2) + 1) % 1000000007
		}
	}
	fmt.Printf("20 rounds of 2000 pairs of 1000 letters: checksum %d\n", check)
}
