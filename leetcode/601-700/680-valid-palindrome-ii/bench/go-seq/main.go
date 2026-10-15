// LeetCode #680: Valid Palindrome II -- two pointers. Bench.
package main

import "fmt"

var seed int64 = 680

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func isPalindrome(b string, i, j int) bool {
	for i < j {
		if b[i] != b[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func validPalindrome(s string) bool {
	i, j := 0, len(s)-1
	for i < j {
		if s[i] != s[j] {
			return isPalindrome(s, i+1, j) || isPalindrome(s, i, j-1)
		}
		i++
		j--
	}
	return true
}

func main() {
	const count, length, rounds = 300, 20000, 100
	widths := []int64{2, 3, 26}
	strings := make([]string, 0, count)
	for k := int64(0); k < count; k++ {
		width := widths[k%3]
		extra := k / 3 % 3
		cs := make([]byte, 0, length+extra)
		for i := 0; i < length/2; i++ {
			cs = append(cs, byte(97+nextRandom()%width))
		}
		for i := length/2 - 1; i >= 0; i-- {
			cs = append(cs, cs[i])
		}
		for e := int64(0); e < extra; e++ {
			at := nextRandom() % int64(len(cs)+1)
			c := byte(97 + nextRandom()%width)
			cs = append(cs, 0)
			copy(cs[at+1:], cs[at:])
			cs[at] = c
		}
		strings = append(strings, string(cs))
	}
	var valid, sum int64
	for r := int64(0); r < rounds; r++ {
		for k := int64(0); k < count; k++ {
			at := (k*7 + r) % count
			if validPalindrome(strings[at]) {
				valid++
				sum = (sum*31 + at + 1) % 1000000007
			} else {
				sum = (sum*31 + 7) % 1000000007
			}
		}
	}
	fmt.Printf("%d strings checked: %d valid, checksum %d\n", count*rounds, valid, sum)
}
