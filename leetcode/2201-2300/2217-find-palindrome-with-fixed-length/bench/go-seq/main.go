// LeetCode #2217: Find Palindrome With Fixed Length -- bench mirror of
// palindrome.kara: the q-th half is 10^(half - 1) + q - 1, mirrored by
// arithmetic, the middle digit of an odd length used once.
package main

import "fmt"

func kthPalindrome(queries []int64, intLength int64) []int64 {
	half := (intLength + 1) / 2
	var low int64 = 1
	for i := int64(1); i < half; i++ {
		low *= 10
	}
	var answer []int64
	for _, q := range queries {
		first := low + q - 1
		if first >= low*10 {
			answer = append(answer, -1)
			continue
		}
		palindrome := first
		rest := first
		if intLength%2 == 1 {
			rest = first / 10
		}
		for rest > 0 {
			palindrome = palindrome*10 + rest%10
			rest /= 10
		}
		answer = append(answer, palindrome)
	}
	return answer
}

var seed int64 = 2217

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

// queries up to twice the count of palindromes of the length, so about
// half of them have none
func query(length int64) int64 {
	var count int64 = 9
	for i := int64(0); i < (length-1)/2; i++ {
		count *= 10
	}
	return wideRandom()%(2*count) + 1
}

func main() {
	var lists [][]int64
	for a := 0; a < 30; a++ {
		// 5 * 10^4 queries for each length from 1 to 15 in turn
		length := int64(a%15 + 1)
		queries := make([]int64, 50000)
		for i := range queries {
			queries[i] = query(length)
		}
		lists = append(lists, queries)
	}
	var check int64
	for a := 0; a < 30; a++ {
		length := int64(a%15 + 1)
		for r := 0; r < 10; r++ {
			// punch: one query is drawn again before each answer
			lists[a][r*4999] = query(length)
			for _, p := range kthPalindrome(lists[a], length) {
				check = (check*31 + p + 1) % 1000000007
			}
		}
	}
	fmt.Printf("30 lists of 5 * 10^4 queries, 10 punches: checksum %d\n", check)
}
