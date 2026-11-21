// LeetCode #2484: Count Palindromic Subsequences -- bench, Go mirror of
// palin.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

const mod = 1000000007

func countPalindromes(s string) int64 {
	digits := make([]int64, len(s))
	for i := range s {
		digits[i] = int64(s[i] - '0')
	}
	beforeOne := make([]int64, 10)
	beforeTwo := make([]int64, 100)
	afterOne := make([]int64, 10)
	afterTwo := make([]int64, 100)
	for i := len(digits) - 1; i >= 0; i-- {
		d := digits[i]
		for a := int64(0); a < 10; a++ {
			afterTwo[d*10+a] += afterOne[a]
		}
		afterOne[d]++
	}
	total := int64(0)
	for _, d := range digits {
		afterOne[d]--
		for a := int64(0); a < 10; a++ {
			afterTwo[d*10+a] -= afterOne[a]
		}
		here := int64(0)
		for a := int64(0); a < 10; a++ {
			for b := int64(0); b < 10; b++ {
				here += beforeTwo[a*10+b] * afterTwo[b*10+a]
			}
		}
		total = (total + here) % mod
		for a := int64(0); a < 10; a++ {
			beforeTwo[a*10+d] += beforeOne[a]
		}
		beforeOne[d]++
	}
	return total
}

var seed int64 = 2484

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strs := make([][]int64, 4)
	for g := range strs {
		strs[g] = make([]int64, 2000)
		for i := range strs[g] {
			strs[g][i] = nextRandom() % 10
		}
	}
	check := int64(0)
	for p := int64(0); p < 110; p++ {
		for g := 0; g < 4; g++ {
			strs[g][check%2000] = check / 2000 % 10
			pieces := make([]string, 2000)
			for i, d := range strs[g] {
				pieces[i] = strconv.FormatInt(d, 10)
			}
			s := strings.Join(pieces, "")
			check = (check*31 + countPalindromes(s) + p) % mod
		}
	}
	fmt.Printf("110 passes over 4 strings of 2000 digits: checksum %d\n", check)
}
