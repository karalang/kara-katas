// LeetCode #2839: Check if Strings Can be Made Equal With Operations I --
// the bench, mirrored from equal.kara: the even pair and the odd pair,
// each either way round.
package main

import "fmt"

func canBeEqual(s1, s2 string) bool {
	a := []rune(s1)
	b := []rune(s2)
	pair := func(x, y, p, q rune) bool { return (x == p && y == q) || (x == q && y == p) }
	return pair(a[0], a[2], b[0], b[2]) && pair(a[1], a[3], b[1], b[3])
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func word(seed *int64) []byte {
	w := make([]byte, 4)
	for i := range w {
		w[i] = byte(97 + nextRandom(seed)%4)
	}
	return w
}

func main() {
	const count, rounds = 1000000, 20
	seed := int64(2839)
	type pairT struct{ a, b string }
	pairs := make([]pairT, 0, count)
	for c := 0; c < count; c++ {
		a := word(&seed)
		var b []byte
		if nextRandom(&seed)%2 == 0 {
			b = append([]byte(nil), a...)
			b[0], b[2] = b[2], b[0]
		} else {
			b = word(&seed)
		}
		pairs = append(pairs, pairT{string(a), string(b)})
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range pairs {
			same := canBeEqual(p.a, p.b)
			v := int64(1)
			if same {
				yes++
				v = 2
			}
			check = (check*31 + v + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs, %d rounds: %d true, checksum %d\n", count, rounds, yes, check)
}
