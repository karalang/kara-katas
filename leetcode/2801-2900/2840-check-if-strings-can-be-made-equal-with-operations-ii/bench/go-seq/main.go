// LeetCode #2840: Check if Strings Can be Made Equal With Operations II
// -- the bench, mirrored from strings.kara: counts in one table of
// 2 x 26, s1 up and s2 down.
package main

import "fmt"

func checkStrings(s1, s2 string) bool {
	count := make([]int64, 52)
	for i := 0; i < len(s1); i++ {
		side := i % 2 * 26
		count[side+int(s1[i]-'a')]++
		count[side+int(s2[i]-'a')]--
	}
	for _, v := range count {
		if v != 0 {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds = 200, 100000, 20
	seed := int64(2840)
	type pairT struct{ a, b string }
	pairs := make([]pairT, 0, count)
	for c := 0; c < count; c++ {
		a := make([]byte, n)
		for i := range a {
			a[i] = byte(97 + nextRandom(&seed)%26)
		}
		b := append([]byte(nil), a...)
		for i := int64(n - 1); i >= 2; i-- {
			j := i%2 + 2*(nextRandom(&seed)%(i/2+1))
			if j <= i {
				b[i], b[j] = b[j], b[i]
			}
		}
		if c%2 == 1 {
			k := nextRandom(&seed) % n
			b[k] = byte(97 + nextRandom(&seed)%26)
		}
		pairs = append(pairs, pairT{string(a), string(b)})
	}
	var yes, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range pairs {
			same := checkStrings(p.a, p.b)
			v := int64(1)
			if same {
				yes++
				v = 2
			}
			check = (check*31 + v + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of %d, %d rounds: %d true, checksum %d\n", count, n, rounds, yes, check)
}
