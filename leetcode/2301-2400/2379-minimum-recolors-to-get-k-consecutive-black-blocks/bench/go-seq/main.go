// LeetCode #2379: Minimum Recolors to Get K Consecutive Black Blocks --
// the bench, the ★ arm in Go: the whites of the first window counted,
// then the window slid along one block at a time.
package main

import "fmt"

func minimumRecolors(b string, k int64) int64 {
	whites := int64(0)
	for i := int64(0); i < k; i++ {
		if b[i] == 'W' {
			whites++
		}
	}
	fewest := whites
	for i := k; i < int64(len(b)); i++ {
		if b[i] == 'W' {
			whites++
		}
		if b[i-k] == 'W' {
			whites--
		}
		if whites < fewest {
			fewest = whites
		}
	}
	return fewest
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 1000 strings of 100 blocks, string s white with a chance of s % 10
	// in 10; pass p asks string s for k = 1 + (7 p + s) % 100
	seed := int64(2379)
	strings := make([]string, 0, 1000)
	for s := int64(0); s < 1000; s++ {
		letters := make([]byte, 100)
		for i := range letters {
			if nextRandom(&seed)%10 < s%10 {
				letters[i] = 'W'
			} else {
				letters[i] = 'B'
			}
		}
		strings = append(strings, string(letters))
	}
	check := int64(0)
	for p := int64(0); p < 500; p++ {
		for s := int64(0); s < 1000; s++ {
			k := 1 + (7*p+s)%100
			check = (check*31 + minimumRecolors(strings[s], k) + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 1000 strings of 100 blocks: checksum %d\n", check)
}
