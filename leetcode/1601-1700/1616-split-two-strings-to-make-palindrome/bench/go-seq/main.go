// LeetCode #1616: Split Two Strings to Make Palindrome -- the bench in
// Go, mirroring split.kara: two pointers, a from the front against b from
// the back as far as they agree, then whether the middle left over, of a
// or of b, is a palindrome by itself; then the roles swapped.
package main

import "fmt"

func isPalindrome(s string, lo, hi int) bool {
	i, j := lo, hi
	for i < j {
		if s[i] != s[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func joins(a, b string) bool {
	i, j := 0, len(a)-1
	for i < j && a[i] == b[j] {
		i++
		j--
	}
	return isPalindrome(a, i, j) || isPalindrome(b, i, j)
}

func checkPalindromeFormation(a, b string) bool {
	return joins(a, b) || joins(b, a)
}

var seed int64 = 1616

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func pair(n int) (string, string) {
	a := make([]byte, n)
	b := make([]byte, n)
	for i := 0; i < n; i++ {
		a[i] = byte('a' + nextRandom()%2)
		b[i] = byte('a' + nextRandom()%2)
	}
	k := int(nextRandom() % int64(n/2+1))
	for j := 0; j < k; j++ {
		b[n-1-j] = a[j]
	}
	for j := 0; j < (n-2*k)/2; j++ {
		b[n-k-1-j] = b[k+j]
	}
	if nextRandom()%2 == 0 {
		i := int(nextRandom() % int64(n))
		b[i] = byte('a' + nextRandom()%2)
	}
	return string(a), string(b)
}

func main() {
	as := make([]string, 10)
	bs := make([]string, 10)
	for p := 0; p < 10; p++ {
		as[p], bs[p] = pair(500000)
	}
	var check, yes int64
	for p := 0; p < 10; p++ {
		for c := 0; c < 30; c++ {
			answer := checkPalindromeFormation(as[p], bs[p])
			if answer {
				yes++
			}
			x := int64(0)
			if answer {
				x = 1
			}
			check = mix(check, x)
		}
	}
	fmt.Printf("10 pairs of 500000 letters from 2, each checked 30 times: %d split, checksum %d\n", yes, check)
}
