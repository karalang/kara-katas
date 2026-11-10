// LeetCode #2108: Find First Palindromic String in the Array -- the
// benchmark, the same algorithm as palindrome.kara: each word's bytes read
// from both ends towards the middle.
package main

import "fmt"

func isPalindrome(w string) bool {
	i, j := 0, len(w)-1
	for i < j {
		if w[i] != w[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func firstPalindrome(words []string) string {
	for _, w := range words {
		if isPalindrome(w) {
			return w
		}
	}
	return ""
}

var seed int64 = 2108

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	lists := make([][]string, 0, 200)
	for l := 0; l < 200; l++ {
		words := make([]string, 0, 100)
		for w := 0; w < 100; w++ {
			letters := make([]int64, 100)
			for i := 0; i < 50; i++ {
				letters[i] = nextRandom() % 26
			}
			for i := 0; i < 50; i++ {
				letters[50+i] = letters[49-i]
			}
			if nextRandom()%200 != 0 {
				at := 25 + nextRandom()%50
				letters[at] = (letters[at] + 1 + nextRandom()%25) % 26
			}
			b := make([]byte, 100)
			for i, x := range letters {
				b[i] = alphabet[x]
			}
			words = append(words, string(b))
		}
		lists = append(lists, words)
	}
	var found, lettersTotal, check int64
	for r := 0; r < 50; r++ {
		for _, words := range lists {
			got := firstPalindrome(words)
			if len(got) > 0 {
				found++
			}
			lettersTotal += int64(len(got))
			for i := 0; i < len(got) && i < 3; i++ {
				check = (check*31 + int64(got[i])) % 1000000007
			}
			check = (check*31 + int64(len(got))) % 1000000007
		}
	}
	fmt.Printf("10000 searches: %d found, %d letters, checksum %d\n", found, lettersTotal, check)
}
