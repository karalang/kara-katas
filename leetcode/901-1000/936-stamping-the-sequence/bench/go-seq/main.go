// LeetCode #936: Stamping The Sequence -- bench: stamps peeled off in
// reverse. Mirrors moves_to_stamp.kara, .c, .rs and .py.
package main

import "fmt"

func movesToStamp(s []byte, target []byte) []int64 {
	t := append([]byte(nil), target...)
	m := len(s)
	n := len(t)
	erased := 0
	order := []int64{}
	progress := true
	for progress && erased < n {
		progress = false
		for p := 0; p < n-m+1; p++ {
			fits := true
			fresh := false
			for k := 0; k < m; k++ {
				if t[p+k] == s[k] {
					fresh = true
				} else if t[p+k] != '?' {
					fits = false
				}
			}
			if fits && fresh {
				for k := 0; k < m; k++ {
					if t[p+k] != '?' {
						t[p+k] = '?'
						erased++
					}
				}
				order = append(order, int64(p))
				progress = true
			}
		}
	}
	if erased < n {
		return []int64{}
	}
	for i, j := 0, len(order)-1; i < j; i, j = i+1, j-1 {
		order[i], order[j] = order[j], order[i]
	}
	return order
}

var seed int64 = 936

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 100
	const count = 50
	const n = 1000
	stamps := [][]byte{}
	targets := [][]byte{}
	for c := 0; c < count; c++ {
		m := 5 + nextRandom()%16
		s := make([]byte, m)
		for k := int64(0); k < m; k++ {
			s[k] = byte(97 + nextRandom()%3)
		}
		out := make([]byte, n)
		for i := range out {
			out[i] = '?'
		}
		left := int64(n)
		for left > 0 {
			p := nextRandom() % (n - m + 1)
			for k := int64(0); k < m; k++ {
				if out[p+k] == '?' {
					left--
				}
				out[p+k] = s[k]
			}
		}
		if c%2 == 1 {
			at := nextRandom() % n
			out[at] = byte(97 + nextRandom()%3)
		}
		stamps = append(stamps, s)
		targets = append(targets, out)
	}
	var stamped, turns, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			c := (r + i) % count
			moves := movesToStamp(stamps[c], targets[c])
			if len(moves) > 0 {
				stamped++
			}
			turns += int64(len(moves))
			for _, p := range moves {
				check = (check*1000003 + p + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d targets of %d letters: %d stamped, %d stamps, checksum %d\n", rounds, count, n, stamped, turns, check)
}
