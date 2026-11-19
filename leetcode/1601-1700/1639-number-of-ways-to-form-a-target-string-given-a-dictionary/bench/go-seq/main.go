// LeetCode #1639: Number of Ways to Form a Target String Given a
// Dictionary -- the bench's Go mirror: the ★ arm on 40 random
// dictionaries of 1000 words of 1000 letters and targets of 500 letters,
// all over the letters a to e and drawn first.
package main

import "fmt"

const modulus = 1000000007

func numWays(words []string, target string) int64 {
	length := len(words[0])
	ways := make([]int64, len(target)+1)
	ways[0] = 1
	for column := 0; column < length; column++ {
		var count [26]int64
		for _, word := range words {
			count[word[column]-'a']++
		}
		for i := min(column+1, len(target)) - 1; i >= 0; i-- {
			have := count[target[i]-'a']
			ways[i+1] = (ways[i+1] + ways[i]*have) % modulus
		}
	}
	return ways[len(target)]
}

var seed int64 = 1639

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length int) string {
	word := make([]byte, length)
	for i := range word {
		word[i] = byte('a' + nextRandom()%5)
	}
	return string(word)
}

func main() {
	type dictionary struct {
		words  []string
		target string
	}
	cases := make([]dictionary, 40)
	for c := range cases {
		words := make([]string, 1000)
		for i := range words {
			words[i] = randomWord(1000)
		}
		cases[c] = dictionary{words, randomWord(500)}
	}
	var check int64
	for _, c := range cases {
		ways := numWays(c.words, c.target)
		check = (check*31 + ways + 1) % 1000000007
	}
	fmt.Printf("40 dictionaries of 1000 words: checksum %d\n", check)
}
