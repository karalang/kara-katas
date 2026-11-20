// LeetCode #2399: Check Distances Between Same Letters -- the bench, the
// ★ arm in Go: the first index of each letter, checked at its second.

package main

import "fmt"

var seed int64 = 2399

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func checkDistances(s string, distance []int64) bool {
	var first [26]int64
	for c := range first {
		first[c] = -1
	}
	for i := 0; i < len(s); i++ {
		c := s[i] - 'a'
		if first[c] < 0 {
			first[c] = int64(i)
		} else if int64(i)-first[c]-1 != distance[c] {
			return false
		}
	}
	return true
}

// All 26 letters, each twice, shuffled, and the distances true of it;
// when off, one letter's distance is one away from its true one.
func makeCase(off bool) (string, []int64) {
	b := make([]byte, 52)
	for i := range b {
		b[i] = byte('a' + i/2)
	}
	for i := int64(1); i < 52; i++ {
		j := nextRandom() % (i + 1)
		b[i], b[j] = b[j], b[i]
	}
	distance := make([]int64, 26)
	var first [26]int64
	for c := range first {
		first[c] = -1
	}
	for i := 0; i < 52; i++ {
		c := b[i] - 'a'
		if first[c] < 0 {
			first[c] = int64(i)
		} else {
			distance[c] = int64(i) - first[c] - 1
		}
	}
	if off {
		letter := nextRandom() % 26
		if distance[letter] == 0 {
			distance[letter]++
		} else {
			distance[letter]--
		}
	}
	return string(b), distance
}

func main() {
	strs := make([]string, 1000)
	dists := make([][]int64, 1000)
	for i := 0; i < 1000; i++ {
		strs[i], dists[i] = makeCase(i%2 == 1)
	}
	var check, yes int64
	for p := int64(0); p < 2000; p++ {
		for i := 0; i < 1000; i++ {
			answer := checkDistances(strs[i], dists[i])
			v := int64(1)
			if answer {
				yes++
				v = 2
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("2000 passes over 1000 strings of 52 letters: checksum %d, %d yes\n", check, yes)
}
