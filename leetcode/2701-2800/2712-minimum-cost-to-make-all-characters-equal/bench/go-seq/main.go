// LeetCode #2712: Minimum Cost to Make All Characters Equal -- the bench
// (equal.kara in Go): each boundary between unequal neighbours priced at
// the cheaper flip across it.
package main

import "fmt"

func minimumCost(s string) int64 {
	n := int64(len(s))
	var cost int64
	for i := int64(1); i < n; i++ {
		if s[i] != s[i-1] {
			if i < n-i {
				cost += i
			} else {
				cost += n - i
			}
		}
	}
	return cost
}

var seed int64 = 2712

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 100, 5
	strings := make([]string, 0, count)
	for c := 0; c < count; c++ {
		change := nextRandom() % 9
		b := make([]byte, 100000)
		last := byte('0')
		for i := range b {
			if nextRandom()%8 < change {
				if last == '0' {
					last = '1'
				} else {
					last = '0'
				}
			}
			b[i] = last
		}
		strings = append(strings, string(b))
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			cost := minimumCost(s)
			sum += cost
			check = (check*31 + cost + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d strings of 100000 bits, %d rounds: costs sum to %d, checksum %d\n", count, rounds, sum, check)
}
