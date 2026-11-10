// LeetCode #2060: Check if an Original String Exists Given Two Encoded
// Strings -- Go mirror of the ★ arm's benchmark (original.kara): the same
// 2000 pairs, each answered by one search over (place, place, lead) with a
// set of the states tried.
package main

import "fmt"

type state struct{ i, j, lead int64 }

func isDigit(c byte) bool { return c >= '0' && c <= '9' }

func search(a, b []byte, i, j, lead int64, seen map[state]bool) bool {
	na, nb := int64(len(a)), int64(len(b))
	if i == na && j == nb {
		return lead == 0
	}
	key := state{i, j, lead}
	if seen[key] {
		return false
	}
	seen[key] = true
	if i < na && isDigit(a[i]) {
		num, k := int64(0), i
		for k < na && isDigit(a[k]) {
			num = num*10 + int64(a[k]-'0')
			k++
			if search(a, b, k, j, lead+num, seen) {
				return true
			}
		}
		return false
	}
	if j < nb && isDigit(b[j]) {
		num, k := int64(0), j
		for k < nb && isDigit(b[k]) {
			num = num*10 + int64(b[k]-'0')
			k++
			if search(a, b, i, k, lead-num, seen) {
				return true
			}
		}
		return false
	}
	if lead > 0 {
		return j < nb && search(a, b, i, j+1, lead-1, seen)
	}
	if lead < 0 {
		return i < na && search(a, b, i+1, j, lead+1, seen)
	}
	return i < na && j < nb && a[i] == b[j] && search(a, b, i+1, j+1, 0, seen)
}

func possiblyEquals(s1, s2 []byte) bool {
	return search(s1, s2, 0, 0, 0, map[state]bool{})
}

var seed int64 = 2060

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func dense() []byte {
	s := []byte{}
	for {
		n := nextRandom()%3 + 1
		run := []byte{}
		for q := int64(0); q < n; q++ {
			run = append(run, byte('1'+nextRandom()%9))
		}
		letter := byte('v')
		if nextRandom()%2 == 0 {
			letter = 'u'
		}
		if len(s)+len(run)+1 > 40 {
			return s
		}
		s = append(s, run...)
		s = append(s, letter)
	}
}

func main() {
	possible := 0
	check := int64(0)
	for t := 0; t < 2000; t++ {
		s1 := dense()
		s2 := dense()
		ok := possiblyEquals(s1, s2)
		if ok {
			possible++
		}
		v := int64(1)
		if ok {
			v = 2
		}
		check = (check*31 + v) % 1000000007
	}
	fmt.Printf("2000 pairs: %d possible, checksum %d\n", possible, check)
}
