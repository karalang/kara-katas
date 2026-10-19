// LeetCode 784 — Letter Case Permutation: the bench, in Go.
// Mirrors letter_case_permutation.kara: backtracking over the same 64
// strings.
package main

import "fmt"

func isAlpha(c byte) bool { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') }

func lower(c byte) byte {
	if c >= 'A' && c <= 'Z' {
		return c + 32
	}
	return c
}

func upper(c byte) byte {
	if c >= 'a' && c <= 'z' {
		return c - 32
	}
	return c
}

func permute(at int, buf []byte, out *[]string) {
	if at == len(buf) {
		*out = append(*out, string(buf))
		return
	}
	c := buf[at]
	if isAlpha(c) {
		buf[at] = lower(c)
		permute(at+1, buf, out)
		buf[at] = upper(c)
		permute(at+1, buf, out)
		buf[at] = c
	} else {
		permute(at+1, buf, out)
	}
}

func letterCasePermutation(s string) []string {
	buf := []byte(s)
	out := []string{}
	permute(0, buf, &out)
	return out
}

var seed int64 = 784

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits := "0123456789"
	strings := make([]string, 0, 64)
	for t := 0; t < 64; t++ {
		wanted := 6 + nextRandom()%6
		isLetter := make([]bool, 12)
		for i := range isLetter {
			isLetter[i] = int64(i) < wanted
		}
		for i := int64(11); i > 0; i-- {
			j := nextRandom() % (i + 1)
			isLetter[i], isLetter[j] = isLetter[j], isLetter[i]
		}
		s := make([]byte, 12)
		for i := 0; i < 12; i++ {
			if isLetter[i] {
				s[i] = letters[nextRandom()%52]
			} else {
				s[i] = digits[nextRandom()%10]
			}
		}
		strings = append(strings, string(s))
	}
	const rounds int64 = 20000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		all := letterCasePermutation(strings[r%64])
		total += int64(len(all))
		for _, w := range all {
			check = (check*31 + int64(w[0]) + 7*int64(w[11])) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 12-character strings: %d permutations, checksum %d\n", rounds, total, check)
}
