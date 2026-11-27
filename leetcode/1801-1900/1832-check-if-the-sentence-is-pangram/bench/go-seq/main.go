// LeetCode #1832: Check if the Sentence Is Pangram -- the bench in Go: the ★
// arm over 100000 calls on runs of 500 to 999 letters cut from one string of
// 2000 letters, built once, each letter a z one time in 600 and otherwise one
// of a to y; each run's start and length are drawn from the checksum so far.
// Each call makes its run a string of its own.
package main

import "fmt"

func checkIfPangram(sentence string) bool {
	var seen int64
	for i := 0; i < len(sentence); i++ {
		seen |= 1 << (sentence[i] - 'a')
	}
	return seen == 1<<26-1
}

var seed int64 = 1832

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := make([]byte, 0, 2000)
	for i := 0; i < 2000; i++ {
		if nextRandom()%600 == 0 {
			letters = append(letters, 'z')
		} else {
			letters = append(letters, byte('a'+nextRandom()%25))
		}
	}
	var check, pangrams int64
	for call := int64(0); call < 100000; call++ {
		start := (check + call) % 1000
		length := 500 + (check*7+call)%500
		yes := checkIfPangram(string(letters[start : start+length]))
		if yes {
			pangrams++
		}
		answer := int64(1)
		if yes {
			answer = 2
		}
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("100000 calls: %d pangrams, checksum %d\n", pangrams, check)
}
