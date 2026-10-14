// Benchmark for #639: mirror of decode_ways_ii.kara (the ★ arm: the count
// of decodings of every prefix, two at a time) on the same workload.
package main

import "fmt"

const m = 1000000007
const rounds = 600

func alone(c byte) int64 {
	if c == '*' {
		return 9
	} else if c == '0' {
		return 0
	}
	return 1
}

func together(a, b byte) int64 {
	if a == '*' {
		if b == '*' {
			return 15
		} else if b <= '6' {
			return 2
		}
		return 1
	} else if a == '1' {
		if b == '*' {
			return 9
		}
		return 1
	} else if a == '2' {
		if b == '*' {
			return 6
		} else if b <= '6' {
			return 1
		}
		return 0
	}
	return 0
}

func numDecodings(s string) int64 {
	var before int64 = 1
	last := alone(s[0])
	for i := 1; i < len(s); i++ {
		next := (last*alone(s[i]) + before*together(s[i-1], s[i])) % m
		before = last
		last = next
	}
	return last
}

var seed int64 = 639

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var texts []string
	for t := 0; t < 20; t++ {
		s := make([]byte, 0, 100000)
		var prev byte = '1'
		for i := 0; i < 100000; i++ {
			var c byte = '*'
			if nextRandom()%10 >= 3 {
				c = byte('1' + nextRandom()%9)
				if nextRandom()%100 == 0 && (prev == '1' || prev == '2' || prev == '*') {
					c = '0'
				}
			}
			s = append(s, c)
			prev = c
		}
		texts = append(texts, string(s))
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		count := numDecodings(texts[round%20])
		total = (total + count) % m
		checksum = (checksum*31 + count) % m
	}
	fmt.Printf("20 strings of 100000 characters, %d rounds: total %d, checksum %d\n", rounds, total, checksum)
}
