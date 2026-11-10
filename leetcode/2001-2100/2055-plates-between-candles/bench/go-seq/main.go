// LeetCode #2055: Plates Between Candles -- Go mirror of the ★ arm's
// benchmark (plates.kara): the same 50 strings and five million queries,
// the string collected into a `[]rune` as the Kāra arm does, the same plate
// counts and nearest candles.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2055

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

type query struct{ left, right int64 }

func platesBetweenCandles(s string, queries []query) []int64 {
	places := []rune(s)
	n := int64(len(places))
	plates := make([]int64, n+1)
	before := make([]int64, n)
	last := int64(-1)
	for i := int64(0); i < n; i++ {
		add := int64(0)
		if places[i] == '*' {
			add = 1
		}
		plates[i+1] = plates[i] + add
		if places[i] == '|' {
			last = i
		}
		before[i] = last
	}
	after := make([]int64, n)
	next := n
	for i := n - 1; i >= 0; i-- {
		if places[i] == '|' {
			next = i
		}
		after[i] = next
	}
	answers := make([]int64, 0, len(queries))
	for _, q := range queries {
		first, lst := after[q.left], before[q.right]
		if first < lst {
			answers = append(answers, plates[lst]-plates[first])
		} else {
			answers = append(answers, 0)
		}
	}
	return answers
}

func main() {
	var total, check int64
	for t := int64(0); t < 50; t++ {
		every := t + 1
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			if nextRandom()%every == 0 {
				b.WriteByte('|')
			} else {
				b.WriteByte('*')
			}
		}
		queries := make([]query, 0, 100000)
		for i := 0; i < 100000; i++ {
			a := wide() % 100000
			c := wide() % 100000
			queries = append(queries, query{min(a, c), max(a, c)})
		}
		for _, a := range platesBetweenCandles(b.String(), queries) {
			total += a
			check = (check*31 + a + 1) % 1000000007
		}
	}
	fmt.Printf("50 strings: sum %d, checksum %d\n", total, check)
}
