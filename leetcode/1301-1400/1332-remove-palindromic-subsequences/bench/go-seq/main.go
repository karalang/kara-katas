// LeetCode #1332 bench, Go mirror of the Kāra bench: the ★ arm on 1000
// strings of 1000 letters built once, then 500 passes, each setting one
// letter of one string from the checksum so far, rebuilding that string,
// and answering every string.
package main

import "fmt"

func removePalindromeSub(s string) int {
	n := len(s)
	for i := 0; i < n/2; i++ {
		if s[i] != s[n-1-i] {
			return 2
		}
	}
	return 1
}

var seed int64 = 1332

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 1000
	const n = 1000
	letters := make([][]byte, count)
	strings := make([]string, count)
	for t := 0; t < count; t++ {
		row := make([]byte, n)
		for i := range row {
			row[i] = 'a'
		}
		for i := 0; i < n/2; i++ {
			c := byte('b')
			if nextRandom()%2 == 0 {
				c = 'a'
			}
			row[i] = c
			row[n-1-i] = c
		}
		if t%2 == 1 {
			k := n/2 - 1 - t%3
			if row[k] == 'a' {
				row[k] = 'b'
			} else {
				row[k] = 'a'
			}
		}
		strings[t] = string(row)
		letters[t] = row
	}
	var check int64
	for pass := int64(0); pass < 500; pass++ {
		t := check % count
		at := check / count % n
		c := byte('b')
		if check/7%2 == 0 {
			c = 'a'
		}
		letters[t][at] = c
		if pass%2 == 0 {
			letters[t][n-1-at] = c
		}
		strings[t] = string(letters[t])
		for _, s := range strings {
			check = (check*31 + int64(removePalindromeSub(s)) + pass) % 1000000007
		}
	}
	fmt.Printf("500 passes over 1000 strings of 1000 letters: checksum %d\n", check)
}
