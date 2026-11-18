// LeetCode #2299: Strong Password Checker II -- the bench, the ★ arm in
// Go. One pass over the letters: a switch sets one of four flags, and the
// letter before must differ from each one.
package main

import "fmt"

func strongPasswordCheckerII(password string) bool {
	if len(password) < 8 {
		return false
	}
	lower, upper, digit, special := false, false, false, false
	prev := ' '
	for _, c := range password {
		if c == prev {
			return false
		}
		switch {
		case c >= 'a' && c <= 'z':
			lower = true
		case c >= 'A' && c <= 'Z':
			upper = true
		case c >= '0' && c <= '9':
			digit = true
		default:
			switch c {
			case '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+':
				special = true
			}
		}
		prev = c
	}
	return lower && upper && digit && special
}

var seed int64 = 2299

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	kinds := []string{
		"abcdefghijklmnopqrstuvwxyz",
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
		"0123456789",
		"!@#$%^&*()-+",
	}
	passwords := make([]string, 0, 200000)
	for k := 0; k < 200000; k++ {
		n := nextRandom()%13 + 8
		width := nextRandom()%12 + 1
		s := make([]byte, 0, n)
		for j := int64(0); j < n; j++ {
			kind := kinds[nextRandom()%4]
			w := width
			if int64(len(kind)) < w {
				w = int64(len(kind))
			}
			s = append(s, kind[nextRandom()%w])
		}
		passwords = append(passwords, string(s))
	}
	count := len(passwords)
	var check int64
	for p := 0; p < 20; p++ {
		for i := 0; i < count; i++ {
			w := passwords[(i+7*p)%count]
			v := int64(1)
			if strongPasswordCheckerII(w) {
				v = int64(len(w))
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("20 passes over 2 * 10^5 passwords: checksum %d\n", check)
}
