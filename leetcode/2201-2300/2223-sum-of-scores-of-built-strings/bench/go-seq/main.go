// LeetCode #2223: Sum of Scores of Built Strings -- bench mirror of
// scores.kara: the Z-function by the Z-algorithm, z[0] = n, summed.
package main

import "fmt"

func sumScores(s string) int64 {
	n := len(s)
	z := make([]int, n)
	z[0] = n
	l, r := 0, 0
	for i := 1; i < n; i++ {
		if i < r {
			z[i] = r - i
			if z[i-l] < z[i] {
				z[i] = z[i-l]
			}
		}
		for i+z[i] < n && s[z[i]] == s[i+z[i]] {
			z[i]++
		}
		if i+z[i] > r {
			l = i
			r = i + z[i]
		}
	}
	var total int64
	for _, v := range z {
		total += int64(v)
	}
	return total
}

var seed int64 = 2223

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func letter() byte {
	if nextRandom()%2 == 1 {
		return 'b'
	}
	return 'a'
}

func main() {
	var words [][]byte
	for a := 0; a < 20; a++ {
		// 10^5 letters, each 'a' or 'b'
		word := make([]byte, 100000)
		for i := range word {
			word[i] = letter()
		}
		words = append(words, word)
	}
	var check int64
	for a := 0; a < 20; a++ {
		for r := 0; r < 5; r++ {
			// punch: one letter is drawn again before each answer
			words[a][r*19999] = letter()
			s := string(words[a])
			check = (check*31 + sumScores(s)) % 1000000007
		}
	}
	fmt.Printf("20 strings of 10^5, 5 punches: checksum %d\n", check)
}
