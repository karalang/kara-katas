// Benchmark for #678: the range of open counts, the ★ arm.
package main

import "fmt"

func checkValidString(s []byte) bool {
	low, high := int64(0), int64(0)
	for _, c := range s {
		if c == '(' {
			low++
			high++
		} else if c == ')' {
			low--
			high--
		} else {
			low--
			high++
		}
		if high < 0 {
			return false
		}
		if low < 0 {
			low = 0
		}
	}
	return low == 0
}

var seed int64 = 678

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomString(c int64) []byte {
	s := []byte{}
	if c%3 == 0 {
		n := 1 + nextRandom()%100
		for i := int64(0); i < n; i++ {
			d := nextRandom() % 3
			if d == 0 {
				s = append(s, '(')
			} else if d == 1 {
				s = append(s, ')')
			} else {
				s = append(s, '*')
			}
		}
		return s
	}
	left := 1 + nextRandom()%50
	open := int64(0)
	b := []byte{}
	for left > 0 || open > 0 {
		if left > 0 && (open == 0 || nextRandom()%2 == 0) {
			b = append(b, '(')
			open++
			left--
		} else {
			b = append(b, ')')
			open--
		}
	}
	stars := nextRandom() % 4
	changes := nextRandom() % 3
	for _, ch := range b {
		r := nextRandom() % 10
		if r < stars {
			s = append(s, '*')
		} else if r == 9 && nextRandom()%3 < changes {
			if ch == '(' {
				s = append(s, ')')
			} else {
				s = append(s, '(')
			}
		} else {
			s = append(s, ch)
		}
	}
	return s
}

func main() {
	const count, rounds = int64(20000), int64(100)
	strings := make([][]byte, count)
	for c := int64(0); c < count; c++ {
		strings[c] = randomString(c)
	}
	sum, valid := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		for i := int64(0); i < count; i++ {
			k := (i*7919 + r*104729) % count
			n := int64(len(strings[k]))
			if checkValidString(strings[k]) {
				valid++
				sum = (sum*31 + n) % 1000000007
			} else {
				sum = (sum*31 + 1000 + n) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds of %d strings: %d valid, checksum %d\n", rounds, count, valid, sum)
}
