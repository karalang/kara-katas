// LeetCode #2131: Longest Palindrome by Concatenating Two Letter Words --
// the benchmark, the same algorithm as palindrome.kara.
package main

import "fmt"

func longestPalindrome(words []string) int64 {
	var count [26 * 26]int64
	for _, w := range words {
		count[int(w[0]-97)*26+int(w[1]-97)]++
	}
	var length int64
	middle := false
	for x := 0; x < 26; x++ {
		length += count[x*26+x] / 2 * 4
		if count[x*26+x]%2 == 1 {
			middle = true
		}
		for y := x + 1; y < 26; y++ {
			length += min(count[x*26+y], count[y*26+x]) * 4
		}
	}
	if middle {
		length += 2
	}
	return length
}

var seed int64 = 2131

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word() string {
	letters := "abcdefgh"
	a := nextRandom() % 8
	b := nextRandom() % 8
	return string([]byte{letters[a], letters[b]})
}

func main() {
	lists := make([][]string, 20)
	for k := range lists {
		lists[k] = make([]string, 100000)
		for i := range lists[k] {
			lists[k][i] = word()
		}
	}
	var total, check int64
	for round := int64(0); round < 10; round++ {
		for k := 0; k < 20; k++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % 100000
			lists[k][at] = word()
			length := longestPalindrome(lists[k])
			total += length
			check = (check*31 + length + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d letters in all, checksum %d\n", total, check)
}
