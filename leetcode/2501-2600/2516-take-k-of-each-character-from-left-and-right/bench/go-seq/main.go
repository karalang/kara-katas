// LeetCode #2516: Take K of Each Character From Left and Right -- Go
// mirror of the benchmark (take.kara): the same strings, passes, order
// and checksum.
package main

import "fmt"

func takeCharacters(s []byte, k int64) int64 {
	n := int64(len(s))
	var total [3]int64
	for _, b := range s {
		total[b-'a']++
	}
	if total[0] < k || total[1] < k || total[2] < k {
		return -1
	}
	var inside [3]int64
	left, longest := int64(0), int64(0)
	for right := int64(0); right < n; right++ {
		c := s[right] - 'a'
		inside[c]++
		for total[c]-inside[c] < k {
			inside[s[left]-'a']--
			left++
		}
		if right-left+1 > longest {
			longest = right - left + 1
		}
	}
	return n - longest
}

var seed int64 = 2516

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([][]byte, 40)
	for t := range strings {
		strings[t] = make([]byte, 100000)
		for i := range strings[t] {
			strings[t][i] = byte('a' + nextRandom()%3)
		}
	}
	const passes = 7
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, s := range strings {
			check = (check*31 + takeCharacters(s, check%30001) + 1 + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 40 strings of 10^5: checksum %d\n", passes, check)
}
