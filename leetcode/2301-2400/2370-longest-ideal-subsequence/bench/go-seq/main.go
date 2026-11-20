// LeetCode #2370: Longest Ideal Subsequence -- the bench, the ★ arm in Go:
// best[c] is the longest ideal subsequence so far ending in letter c, and
// a new letter extends the best one within k letters of it.
package main

import "fmt"

func longestIdealString(s string, k int64) int64 {
	best := make([]int64, 26)
	for i := 0; i < len(s); i++ {
		c := int64(s[i] - 'a')
		lo := max(c-k, 0)
		hi := min(c+k, 25)
		most := int64(0)
		for d := lo; d <= hi; d++ {
			most = max(most, best[d])
		}
		best[c] = most + 1
	}
	top := int64(0)
	for _, b := range best {
		top = max(top, b)
	}
	return top
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// string a: 10^5 random letters from the whole alphabet, answered with
	// k of a and of 2 a + 5
	seed := int64(2370)
	strings := make([]string, 0, 10)
	for a := 0; a < 10; a++ {
		bytes := make([]byte, 100000)
		for i := range bytes {
			bytes[i] = byte(97 + nextRandom(&seed)%26)
		}
		strings = append(strings, string(bytes))
	}
	check := int64(0)
	for p := int64(0); p < 10; p++ {
		for a := int64(0); a < 10; a++ {
			for _, k := range []int64{a, 2*a + 5} {
				check = (check*31 + longestIdealString(strings[a], k) + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 10 strings of 10^5 letters: checksum %d\n", check)
}
