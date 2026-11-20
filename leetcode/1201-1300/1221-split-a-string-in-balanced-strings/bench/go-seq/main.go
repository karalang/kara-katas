// LeetCode #1221 bench, Go mirror of the Kāra ★ arm: walk the string
// keeping L's count less R's and count the returns to zero, over 2000
// random balanced strings of 1000 letters drawn once, 20 passes; checksum
// of the answers.
package main

import "fmt"

var seed int64 = 1221

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func balancedStringSplit(s string) int64 {
	var balance, pieces int64
	for _, c := range s {
		if c == 'L' {
			balance++
		} else {
			balance--
		}
		if balance == 0 {
			pieces++
		}
	}
	return pieces
}

func main() {
	strings := make([]string, 0, 2000)
	for i := 0; i < 2000; i++ {
		letters := make([]byte, 0, 1000)
		for k := 0; k < 500; k++ {
			letters = append(letters, 'L', 'R')
		}
		for k := int64(len(letters) - 1); k > 0; k-- {
			j := nextRandom() % (k + 1)
			letters[k], letters[j] = letters[j], letters[k]
		}
		strings = append(strings, string(letters))
	}
	var total, check int64
	for pass := 0; pass < 20; pass++ {
		for _, s := range strings {
			answer := balancedStringSplit(s)
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("2000 strings of 1000 letters, 20 passes: pieces total %d, checksum %d\n", total, check)
}
