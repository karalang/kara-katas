// Benchmark for #777: Swap Adjacent in LR String -- mirror of the ★ arm
// (two pointers), with the same workload as the Kāra program.
package main

import "fmt"

func canTransform(s, e string) bool {
	n := len(s)
	if len(e) != n {
		return false
	}
	i, j := 0, 0
	for {
		for i < n && s[i] == 'X' {
			i++
		}
		for j < n && e[j] == 'X' {
			j++
		}
		if i == n || j == n {
			return i == n && j == n
		}
		if s[i] != e[j] {
			return false
		}
		if s[i] == 'L' && i < j {
			return false
		}
		if s[i] == 'R' && i > j {
			return false
		}
		i++
		j++
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const n = 10000
	seed := int64(777)
	starts := make([]string, 0, count)
	ends := make([]string, 0, count)
	for g := 0; g < count; g++ {
		s := make([]byte, n)
		for i := range s {
			r := nextRandom(&seed) % 4
			if r < 2 {
				s[i] = 'X'
			} else if r == 2 {
				s[i] = 'L'
			} else {
				s[i] = 'R'
			}
		}
		e := append([]byte(nil), s...)
		if g%4 < 2 {
			for m := 0; m < 100000; m++ {
				i := int(nextRandom(&seed) % (n - 1))
				if (e[i] == 'X' && e[i+1] == 'L') || (e[i] == 'R' && e[i+1] == 'X') {
					e[i], e[i+1] = e[i+1], e[i]
				}
			}
		} else {
			var k int
			if g%4 == 2 {
				k = n - 2
			} else {
				k = int(nextRandom(&seed) % (n - 1))
			}
			for !(e[k] == 'X' && e[k+1] == 'R') {
				if k == 0 {
					k = n - 2
				} else {
					k--
				}
			}
			e[k], e[k+1] = e[k+1], e[k]
		}
		starts = append(starts, string(s))
		ends = append(ends, string(e))
	}
	yes := 0
	checksum := int64(0)
	for round := 0; round < 20000; round++ {
		g := (round * 7) % count
		if canTransform(starts[g], ends[g]) {
			yes++
			checksum = (checksum*31 + int64(g) + 1) % 1000000007
		} else {
			checksum = (checksum*31 + 7) % 1000000007
		}
	}
	fmt.Printf("20000 rounds of %d letters: %d reachable, checksum %d\n", n, yes, checksum)
}
