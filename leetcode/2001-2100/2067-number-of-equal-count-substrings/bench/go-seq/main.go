// LeetCode #2067: Number of Equal Count Substrings -- Go mirror of the
// ★ arm's benchmark (count.kara): 60 texts of 30000 letters from 1 to 26
// kinds, half in runs of `count`, count 1 to 7.
package main

import "fmt"

func equalCountSubstrings(s []byte, count int64) int64 {
	n := int64(len(s))
	total := int64(0)
	for k := int64(1); k <= 26; k++ {
		length := k * count
		if length > n {
			break
		}
		var seen [26]int64
		exact := int64(0)
		for i := int64(0); i < n; i++ {
			c := s[i] - 'a'
			seen[c]++
			if seen[c] == count {
				exact++
			} else if seen[c] == count+1 {
				exact--
			}
			if i >= length {
				d := s[i-length] - 'a'
				if seen[d] == count {
					exact--
				}
				seen[d]--
				if seen[d] == count {
					exact++
				}
			}
			if i+1 >= length && exact == k {
				total++
			}
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func textOf(n, k, count, p int64, seed *int64) []byte {
	out := make([]byte, 0, n)
	length := int64(0)
	for length < n {
		c := byte('a' + nextRandom(seed)%k)
		run := int64(1)
		if nextRandom(seed)%100 < p {
			run = count
		}
		if run > n-length {
			run = n - length
		}
		for j := int64(0); j < run; j++ {
			out = append(out, c)
		}
		length += run
	}
	return out
}

func main() {
	seed := int64(2067)
	total, check := int64(0), int64(0)
	for t := int64(0); t < 60; t++ {
		count := t%7 + 1
		a := equalCountSubstrings(textOf(30000, t%26+1, count, 50, &seed), count)
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("60 texts: sum %d, checksum %d\n", total, check)
}
