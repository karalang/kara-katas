// LeetCode 767 — Reorganize String: benchmark, the ★ arm in Go.
// Sixty-four random strings of 500 letters, built once; 400,000 rounds
// each reorganize the next of them.
package main

import "fmt"

var seed int64 = 767

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func reorganizeString(s string) string {
	n := len(s)
	var counts [26]int
	for i := 0; i < n; i++ {
		counts[s[i]-'a']++
	}
	most := 0
	for k := 1; k < 26; k++ {
		if counts[k] > counts[most] {
			most = k
		}
	}
	if counts[most] > (n+1)/2 {
		return ""
	}
	out := make([]byte, n)
	place := 0
	for step := 0; step < 27; step++ {
		k := step - 1
		if step == 0 {
			k = most
		} else if k == most {
			continue
		}
		for c := 0; c < counts[k]; c++ {
			if place >= n {
				place = 1
			}
			out[place] = byte('a' + k)
			place += 2
		}
	}
	return string(out)
}

func main() {
	rounds := 400000
	pool := make([]string, 64)
	for p := range pool {
		letters := 1 + nextRandom()%26
		bytes := make([]byte, 500)
		for i := range bytes {
			k := nextRandom() % (letters + 1)
			if k == letters {
				k = 0
			}
			bytes[i] = byte('a' + k)
		}
		pool[p] = string(bytes)
	}
	var possible, check int64
	for round := 0; round < rounds; round++ {
		answer := reorganizeString(pool[round%64])
		var letter int64
		if len(answer) > 0 {
			possible++
			letter = int64(answer[round%500])
		}
		check = (check*31 + int64(len(answer)) + letter) % 1000000007
	}
	fmt.Printf("%d strings of 500 letters: %d rearranged, checksum %d\n", rounds, possible, check)
}
