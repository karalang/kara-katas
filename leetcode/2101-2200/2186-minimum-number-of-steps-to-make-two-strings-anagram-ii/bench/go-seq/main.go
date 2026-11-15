// LeetCode #2186: Minimum Number of Steps to Make Two Strings Anagram II
// -- the benchmark's Go mirror of anagram_steps.kara, over slices of the
// row: one balance of 26 counts.
package main

import "fmt"

func minSteps(s, t string) int64 {
	var balance [26]int64
	for i := 0; i < len(s); i++ {
		balance[s[i]-97]++
	}
	for i := 0; i < len(t); i++ {
		balance[t[i]-97]--
	}
	var steps int64
	for _, d := range balance {
		if d < 0 {
			steps -= d
		} else {
			steps += d
		}
	}
	return steps
}

var seed int64 = 2186

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	row := make([]byte, 1000000)
	for i := range row {
		row[i] = byte(97 + nextRandom()%26)
	}
	text := string(row)
	var check int64
	for r := 0; r < 200; r++ {
		a := nextRandom()
		b := nextRandom()
		c := nextRandom()
		d := nextRandom()
		i := (a*32768 + b) % 800001
		j := (c*32768 + d) % 800001
		check = (check*31 + minSteps(text[i:i+200000], text[j:j+200000])) % 1000000007
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
