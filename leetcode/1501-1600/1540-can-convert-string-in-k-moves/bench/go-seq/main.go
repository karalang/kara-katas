// LeetCode #1540: Can Convert String in K Moves -- bench: the ★ arm (the
// places counted by shift) over 100 pairs of 1 to 20000 letters, each with
// k from 0 to 40000, built once, every pair asked 50 times. Go mirror of
// convert.kara.
package main

import "fmt"

func canConvertString(s, t string, k int64) bool {
	if len(s) != len(t) {
		return false
	}
	var count [26]int64
	for i := 0; i < len(s); i++ {
		d := (int64(t[i]) - int64(s[i]) + 26) % 26
		count[d]++
	}
	for d := int64(1); d < 26; d++ {
		if count[d] > 0 && d+26*(count[d]-1) > k {
			return false
		}
	}
	return true
}

var seed int64 = 1540

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func word(n, letters int64) string {
	w := make([]byte, n)
	for i := range w {
		w[i] = byte('a' + nextRandom()%letters)
	}
	return string(w)
}

type pair struct {
	s, t string
	k    int64
}

func main() {
	pairs := make([]pair, 0, 100)
	for p := 0; p < 100; p++ {
		a := nextRandom()
		n := (a*32768+nextRandom())%20000 + 1
		used := nextRandom()%26 + 1
		s := word(n, used)
		t := word(n, used)
		b := nextRandom()
		k := (b*32768 + nextRandom()) % 40001
		pairs = append(pairs, pair{s, t, k})
	}
	check, yes := int64(0), 0
	for r := 0; r < 50; r++ {
		for _, p := range pairs {
			answer := canConvertString(p.s, p.t, p.k)
			x := int64(0)
			if answer {
				yes++
				x = 1
			}
			check = mix(check, x)
		}
	}
	fmt.Printf("50 passes over 100 pairs of up to 20000 letters: %d true, checksum %d\n", yes, check)
}
