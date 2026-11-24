// LeetCode #1316 bench, Go mirror of the Kāra bench: the ★ arm (a table of
// how far every two suffixes agree, each echo counted at the first place it
// starts) on 4 strings of 2000 letters built once; then 5 passes, each
// setting one letter of every string from the checksum so far, answering it
// and folding the count plus the pass into the checksum.
package main

import "fmt"

func distinctEchoSubstrings(text string) int32 {
	s := []byte(text)
	n := len(s)
	agree := make([][]int64, n+1)
	for i := range agree {
		agree[i] = make([]int64, n+1)
	}
	for i := n - 1; i >= 0; i-- {
		for j := n - 1; j > i; j-- {
			if s[i] == s[j] {
				agree[i][j] = agree[i+1][j+1] + 1
			}
		}
	}
	earlier := make([]int64, n)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if agree[i][j] > earlier[j] {
				earlier[j] = agree[i][j]
			}
		}
	}
	var count int64
	for i := 0; i < n; i++ {
		for h := 1; h <= (n-i)/2; h++ {
			if agree[i][i+h] >= int64(h) && int64(2*h) > earlier[i] {
				count++
			}
		}
	}
	return int32(count)
}

var seed int64 = 1316

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 2000
	letters := []byte("abcdefghijklmnopqrstuvwxyz")
	strings := make([][]byte, 4)
	for t := 0; t < 4; t++ {
		chars := make([]byte, n)
		if t == 3 {
			var block [3]byte
			for b := 0; b < 3; b++ {
				block[b] = letters[nextRandom()%26]
			}
			for i := 0; i < n; i++ {
				chars[i] = block[i%3]
			}
		} else {
			k := int64(26)
			if t == 0 {
				k = 2
			} else if t == 1 {
				k = 3
			}
			for i := 0; i < n; i++ {
				chars[i] = letters[nextRandom()%k]
			}
		}
		strings[t] = chars
	}
	var check int64
	for pass := int64(0); pass < 5; pass++ {
		for t := 0; t < 4; t++ {
			strings[t][check%n] = letters[(check/7)%26]
			count := int64(distinctEchoSubstrings(string(strings[t])))
			check = (check*31 + count + pass) % 1000000007
		}
	}
	fmt.Printf("5 passes over 4 strings of 2000: checksum %d\n", check)
}
