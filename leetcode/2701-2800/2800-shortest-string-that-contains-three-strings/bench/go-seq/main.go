// LeetCode #2800: Shortest String That Contains Three Strings -- the
// bench in Go: the ★ arm over 2000 triples of up to 100 letters from a
// and b, all drawn first, then each answered 200 times.
package main

import (
	"fmt"
	"strings"
)

func merge(s, t string) string {
	if strings.Contains(s, t) {
		return s
	}
	k := len(t)
	if len(s) < k {
		k = len(s)
	}
	for ; k >= 1; k-- {
		if strings.HasSuffix(s, t[:k]) {
			return s + t[k:]
		}
	}
	return s + t
}

func minimumString(a, b, c string) string {
	words := [3]string{a, b, c}
	orders := [6][3]int{{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}}
	best := ""
	for _, order := range orders {
		s := merge(merge(words[order[0]], words[order[1]]), words[order[2]])
		if best == "" || len(s) < len(best) || (len(s) == len(best) && s < best) {
			best = s
		}
	}
	return best
}

var seed int64 = 2800

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(m int64) string {
	var w strings.Builder
	for i := int64(0); i < m; i++ {
		w.WriteByte("ab"[nextRandom()%2])
	}
	return w.String()
}

func digest(s string) int64 {
	var h int64
	for i := 0; i < len(s); i++ {
		h = (h*131 + int64(s[i])) % 1000000007
	}
	return h
}

func main() {
	count := 2000
	rounds := 200
	cases := make([][3]string, count)
	for c := 0; c < count; c++ {
		for i := 0; i < 3; i++ {
			cases[c][i] = word(nextRandom()%100 + 1)
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, t := range cases {
			s := minimumString(t[0], t[1], t[2])
			total += int64(len(s))
			check = (check*31 + digest(s) + r) % 1000000007
		}
	}
	fmt.Printf("%d triples of up to 100, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, total, check)
}
