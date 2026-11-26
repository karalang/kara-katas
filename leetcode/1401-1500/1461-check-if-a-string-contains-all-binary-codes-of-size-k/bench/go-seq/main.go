// LeetCode #1461 bench in Go: the ★ arm (the last k digits kept as a
// number, each window marked once) on the same 20 strings of 5 * 10^5
// digits, k from 11 to 20.
package main

import "fmt"

func hasAllCodes(s string, k int) bool {
	need := 1 << k
	seen := make([]bool, need)
	found, window := 0, 0
	for i := 0; i < len(s); i++ {
		window = ((window << 1) | int(s[i]-'0')) & (need - 1)
		if i+1 >= k && !seen[window] {
			seen[window] = true
			found++
			if found == need {
				return true
			}
		}
	}
	return false
}

var seed int64 = 1461

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	texts := make([][]byte, 20)
	for t := range texts {
		texts[t] = make([]byte, 500000)
		for i := range texts[t] {
			if nextRandom()%2 == 0 {
				texts[t][i] = '0'
			} else {
				texts[t][i] = '1'
			}
		}
	}
	var check int64
	for t := 0; t < 20; t++ {
		for k := 11; k <= 20; k++ {
			at := check % 500000
			if texts[t][at] == '0' {
				texts[t][at] = '1'
			} else {
				texts[t][at] = '0'
			}
			s := string(texts[t])
			var all int64
			if hasAllCodes(s, k) {
				all = 1
			}
			check = (check*31 + all + int64(k)) % 1000000007
		}
	}
	fmt.Printf("20 strings of 5 * 10^5 digits, k from 11 to 20: checksum %d\n", check)
}
