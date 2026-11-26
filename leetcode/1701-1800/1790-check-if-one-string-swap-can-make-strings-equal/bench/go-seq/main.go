// LeetCode #1790: Check if One String Swap Can Make Strings Equal -- the
// bench in Go, mirroring are_almost_equal.kara: the positions where the
// strings differ.
package main

import "fmt"

func areAlmostEqual(s1, s2 string) bool {
	differ := make([]int, 0, 3)
	for i := 0; i < len(s1); i++ {
		if s1[i] != s2[i] {
			differ = append(differ, i)
			if len(differ) > 2 {
				return false
			}
		}
	}
	switch len(differ) {
	case 0:
		return true
	case 2:
		return s1[differ[0]] == s2[differ[1]] && s1[differ[1]] == s2[differ[0]]
	}
	return false
}

var seed int64 = 1790

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type pair struct{ a, b string }
	pairs := make([]pair, 0, 2000)
	for k := 0; k < 2000; k++ {
		a := make([]byte, 0, 100)
		for i := 0; i < 100; i++ {
			a = append(a, byte(97+nextRandom()%26))
		}
		b := append([]byte(nil), a...)
		for r := 0; r < k%4; r++ {
			i := nextRandom() % 100
			j := nextRandom() % 100
			if k%4 == 3 {
				b[i] = 97 + (b[i]-97+1)%26
			} else {
				b[i], b[j] = b[j], b[i]
			}
		}
		pairs = append(pairs, pair{string(a), string(b)})
	}
	var check int64
	for call := int64(0); call < 4000000; call++ {
		p := pairs[(check+call)%2000]
		if areAlmostEqual(p.a, p.b) {
			check = (check*3 + 2) % 1000000007
		} else {
			check = (check*3 + 1) % 1000000007
		}
	}
	fmt.Printf("4000000 calls over 2000 pairs: checksum %d\n", check)
}
