// LeetCode #2851: String Transformation -- the bench: the ★ arm over 10
// pairs of 5 * 10^5 letters, LeetCode's most, each s a block of up to 8
// letters repeated, half of them with one letter changed, t a rotation
// of s two times in three and otherwise s with one letter changed, k up
// to about 10^15, all drawn first, then each answered 5 times.
package main

import "fmt"

const mod = 1000000007

func power(base, exp int64) int64 {
	result, b, e := int64(1), base%mod, exp
	for e > 0 {
		if e%2 == 1 {
			result = result * b % mod
		}
		b = b * b % mod
		e /= 2
	}
	return result
}

func numberOfWays(s, t string, k int64) int64 {
	n := len(s)
	text := []byte(s + s)
	pat := []byte(t)
	fail := make([]int, n)
	j := 0
	for i := 1; i < n; i++ {
		for j > 0 && pat[i] != pat[j] {
			j = fail[j-1]
		}
		if pat[i] == pat[j] {
			j++
		}
		fail[i] = j
	}
	var atZero, elsewhere int64
	j = 0
	for i := 0; i < 2*n-1; i++ {
		for j > 0 && text[i] != pat[j] {
			j = fail[j-1]
		}
		if text[i] == pat[j] {
			j++
		}
		if j == n {
			if i+1 == n {
				atZero++
			} else {
				elsewhere++
			}
			j = fail[j-1]
		}
	}
	m := int64(n)
	all := power(m-1, k)
	sign := int64(1)
	if k%2 != 0 {
		sign = mod - 1
	}
	inverse := power(m, mod-2)
	zeroWays := (all + (m-1)*sign) % mod * inverse % mod
	otherWays := (all - sign + mod) % mod * inverse % mod
	return (atZero*zeroWays + elsewhere*otherWays) % mod
}

var seed int64 = 2851

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

type pair struct {
	s, t string
	k    int64
}

func main() {
	const count, rounds, n = 10, 5, 500000
	pairs := []pair{}
	for c := 0; c < count; c++ {
		block := nextRandom()%8 + 1
		letters := nextRandom()%3 + 1
		unit := make([]byte, block)
		for i := range unit {
			unit[i] = byte('a' + nextRandom()%letters)
		}
		s := make([]byte, n)
		for i := range s {
			s[i] = unit[int64(i)%block]
		}
		if nextRandom()%2 == 0 {
			at := wide() % n
			s[at] = byte('a' + nextRandom()%3)
		}
		var t []byte
		if nextRandom()%3 < 2 {
			r := wide() % n
			t = append(append([]byte{}, s[n-r:]...), s[:n-r]...)
		} else {
			t = append([]byte{}, s...)
			at := wide() % n
			t[at] = 'a' + (t[at]-'a'+1)%3
		}
		k := wide()*900000 + 1
		pairs = append(pairs, pair{string(s), string(t), k})
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range pairs {
			check = (check*31 + numberOfWays(p.s, p.t, p.k) + r) % mod
		}
	}
	fmt.Printf("%d pairs of %d, %d rounds: checksum %d\n", count, n, rounds, check)
}
