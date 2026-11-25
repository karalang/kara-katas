// LeetCode #1397 bench -- Go: the strings built a letter at a time,
// counted by how much of `evil` their end matches and whether they are
// still at s1's prefix and at s2's, the matches stepped through a KMP
// automaton table.
package main

import "fmt"

func slot(j int64, low, high bool) int64 {
	s := j * 4
	if low {
		s += 2
	}
	if high {
		s++
	}
	return s
}

func findGoodStrings(n int32, s1, s2, evil string) int32 {
	const modulus = 1000000007
	m := int64(len(evil))
	border := make([]int64, m)
	k := int64(0)
	for i := int64(1); i < m; i++ {
		for k > 0 && evil[i] != evil[k] {
			k = border[k-1]
		}
		if evil[i] == evil[k] {
			k++
		}
		border[i] = k
	}
	next := make([]int64, m*26)
	for j := int64(0); j < m; j++ {
		for c := int64(0); c < 26; c++ {
			if int64(evil[j]) == 97+c {
				next[j*26+c] = j + 1
			} else if j > 0 {
				next[j*26+c] = next[border[j-1]*26+c]
			}
		}
	}
	ways := make([]int64, m*4)
	ways[slot(0, true, true)] = 1
	for i := int32(0); i < n; i++ {
		after := make([]int64, m*4)
		for j := int64(0); j < m; j++ {
			for _, low := range [2]bool{false, true} {
				for _, high := range [2]bool{false, true} {
					w := ways[slot(j, low, high)]
					if w == 0 {
						continue
					}
					first, last := int64(0), int64(25)
					if low {
						first = int64(s1[i]) - 97
					}
					if high {
						last = int64(s2[i]) - 97
					}
					for c := first; c <= last; c++ {
						to := next[j*26+c]
						if to == m {
							continue
						}
						at := slot(to, low && c == first, high && c == last)
						after[at] = (after[at] + w) % modulus
					}
				}
			}
		}
		ways = after
	}
	total := int64(0)
	for _, w := range ways {
		total = (total + w) % modulus
	}
	return int32(total)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1397)
	low := make([]byte, 500)
	high := make([]byte, 500)
	evil := make([]byte, 50)
	for i := range low {
		low[i] = byte(97 + nextRandom(&seed)%3)
	}
	for i := range high {
		high[i] = byte(120 + nextRandom(&seed)%3)
	}
	for i := range evil {
		evil[i] = byte(97 + nextRandom(&seed)%3)
	}
	check := int64(0)
	for r := 0; r < 200; r++ {
		seed = (seed + check) % 2147483648
		at := nextRandom(&seed) % 500
		low[at] = byte(97 + nextRandom(&seed)%3)
		at = nextRandom(&seed) % 500
		high[at] = byte(120 + nextRandom(&seed)%3)
		at = nextRandom(&seed) % 50
		evil[at] = byte(97 + nextRandom(&seed)%3)
		check = (check*131 + int64(findGoodStrings(500, string(low), string(high), string(evil)))) % 1000000007
	}
	fmt.Printf("200 rounds at n = 500, evil of 50 letters: checksum %d\n", check)
}
