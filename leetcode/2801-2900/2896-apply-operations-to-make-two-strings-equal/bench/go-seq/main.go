// LeetCode #2896: Apply Operations to Make Two Strings Equal -- the bench, as
// flips.kara: 5000 pairs of 500 characters, each answered 20 times by
// the pairing arm.
package main

import "fmt"

func minOperations(s1, s2 string, x int64) int64 {
	a, b := []rune(s1), []rune(s2)
	var places []int64
	for i := range a {
		if a[i] != b[i] {
			places = append(places, int64(i))
		}
	}
	m := len(places)
	if m%2 == 1 {
		return -1
	}
	doubled := make([]int64, m+1)
	for i := 1; i <= m; i++ {
		doubled[i] = doubled[i-1] + x
		if i >= 2 {
			doubled[i] = min(doubled[i], doubled[i-2]+2*(places[i-1]-places[i-2]))
		}
	}
	return doubled[m] / 2
}

var seed int64 = 2896

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bits(n int64) string {
	s := make([]byte, n)
	for i := range s {
		if nextRandom()%2 == 0 {
			s[i] = '0'
		} else {
			s[i] = '1'
		}
	}
	return string(s)
}

func main() {
	const count, rounds, n = 5000, 20, 500
	s1s := make([]string, count)
	s2s := make([]string, count)
	xs := make([]int64, count)
	for c := 0; c < count; c++ {
		xs[c] = nextRandom()%500 + 1
		s1s[c] = bits(n)
		if c%2 == 0 {
			s2s[c] = bits(n)
		} else {
			chars := []byte(s1s[c])
			flips := nextRandom() % 20
			for k := int64(0); k < flips; k++ {
				at := nextRandom() % n
				if chars[at] == '0' {
					chars[at] = '1'
				} else {
					chars[at] = '0'
				}
			}
			s2s[c] = string(chars)
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			cost := minOperations(s1s[c], s2s[c], xs[c])
			total += cost
			check = (check*31 + cost + 1 + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of %d, %d rounds: costs total %d, checksum %d\n", count, n, rounds, total, check)
}
