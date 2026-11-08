// LeetCode #1071: Greatest Common Divisor of Strings -- the benchmark's Go
// mirror of gcd_strings.kara: the same concatenations compared over 20000
// pairs built once, each answered 50 times.
package main

import (
	"fmt"
	"strings"
)

func gcd(a, b int) int {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func gcdOfStrings(a, b string) string {
	if a+b != b+a {
		return ""
	}
	return strings.Clone(a[:gcd(len(a), len(b))])
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomWord(n, k int64, seed *int64) string {
	var s strings.Builder
	for i := int64(0); i < n; i++ {
		s.WriteByte(byte('A' + nextRandom(seed)%k))
	}
	return s.String()
}

func main() {
	var seed int64 = 1071
	type pair struct{ a, b string }
	pairs := make([]pair, 0)
	for i := 0; i < 20000; i++ {
		k := nextRandom(&seed)%4 + 1
		root := randomWord(nextRandom(&seed)%20+1, k, &seed)
		a := strings.Repeat(root, int(nextRandom(&seed)%50+1))
		b := strings.Repeat(root, int(nextRandom(&seed)%50+1))
		roll := nextRandom(&seed) % 6
		if roll < 2 {
			at := nextRandom(&seed) % int64(len(b))
			letter := byte('A' + nextRandom(&seed)%k)
			b = b[:at] + string(letter) + b[at+1:]
		} else if roll == 2 {
			b = randomWord(nextRandom(&seed)%1000+1, k, &seed)
		}
		pairs = append(pairs, pair{a, b})
	}
	var found, letters, check int64
	for r := 0; r < 50; r++ {
		for _, p := range pairs {
			x := gcdOfStrings(p.a, p.b)
			if len(x) > 0 {
				found++
			}
			letters += int64(len(x))
			check = (check*31 + int64(len(x))) % 1000000007
		}
	}
	fmt.Printf("1000000 calls: %d found, %d letters, checksum %d\n", found, letters, check)
}
