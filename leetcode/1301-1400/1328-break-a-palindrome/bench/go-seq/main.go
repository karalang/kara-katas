// LeetCode #1328 bench, Go mirror of the Kāra bench: the ★ arm (the letters
// into a []rune, the first half searched for a letter that is not an a, the
// answer converted back into a string) on 20 palindromes of 10^5 letters
// built once, in four kinds: all a; a until the last tenth of the half,
// then random letters; a with a rare b; and random letters. Then 800
// passes, each setting one mirrored pair of every palindrome from the
// checksum so far, answering it and folding two of the answer's letters
// plus the pass into the checksum.
package main

import "fmt"

func breakPalindrome(palindrome string) string {
	chars := []rune(palindrome)
	n := len(chars)
	if n == 1 {
		return ""
	}
	for i := 0; i < n/2; i++ {
		if chars[i] != 'a' {
			chars[i] = 'a'
			return string(chars)
		}
	}
	chars[n-1] = 'b'
	return string(chars)
}

var seed int64 = 1328

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	letters := []byte("abcdefghijklmnopqrstuvwxyz")
	texts := make([][]byte, 0, 20)
	for t := 0; t < 20; t++ {
		kind := t % 4
		bytes := make([]byte, n)
		for i := range bytes {
			bytes[i] = 'a'
		}
		for i := 0; i < n/2; i++ {
			var c byte
			switch {
			case kind == 0:
				c = 'a'
			case kind == 1:
				if i < n/2-n/20 {
					c = 'a'
				} else {
					c = letters[nextRandom()%26]
				}
			case kind == 2:
				if nextRandom()%2000 == 0 {
					c = 'b'
				} else {
					c = 'a'
				}
			default:
				c = letters[nextRandom()%26]
			}
			bytes[i] = c
			bytes[n-1-i] = c
		}
		texts = append(texts, bytes)
	}
	var check int64
	for pass := int64(0); pass < 800; pass++ {
		for t := 0; t < 20; t++ {
			j := check % (n / 2)
			c := byte('a')
			if (check/7)%4 == 0 {
				c = 'b'
			}
			texts[t][j] = c
			texts[t][n-1-j] = c
			got := breakPalindrome(string(texts[t]))
			check = (check*31 + int64(got[j]) + int64(got[n-1]) + pass) % 1000000007
		}
	}
	fmt.Printf("800 passes over 20 palindromes of 10^5: checksum %d\n", check)
}
