// LeetCode #1528: Shuffle String -- bench: the ★ arm over 100000 random
// strings of 1 to 100 letters with shuffled indices, built once and
// answered 30 times.
package main

import "fmt"

func restoreString(s string, indices []int64) string {
	out := make([]byte, len(s))
	for i := 0; i < len(s); i++ {
		out[indices[i]] = s[i]
	}
	return string(out)
}

var seed int64 = 1528

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

type kase struct {
	s       string
	indices []int64
}

func main() {
	cases := make([]kase, 0, 100000)
	for c := 0; c < 100000; c++ {
		n := nextRandom()%100 + 1
		b := make([]byte, n)
		for i := int64(0); i < n; i++ {
			b[i] = byte(97 + nextRandom()%26)
		}
		indices := make([]int64, n)
		for i := int64(0); i < n; i++ {
			indices[i] = i
		}
		for i := n - 1; i >= 1; i-- {
			j := nextRandom() % (i + 1)
			indices[i], indices[j] = indices[j], indices[i]
		}
		cases = append(cases, kase{string(b), indices})
	}
	var check int64
	for pass := 0; pass < 30; pass++ {
		for _, k := range cases {
			answer := restoreString(k.s, k.indices)
			check = mix(check, int64(answer[pass%len(answer)]))
		}
	}
	fmt.Printf("30 passes over 100000 strings of up to 100 letters: checksum %d\n", check)
}
