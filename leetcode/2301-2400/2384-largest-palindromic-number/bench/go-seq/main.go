// LeetCode #2384: Largest Palindromic Number -- the bench, the ★ arm in
// Go: the digits counted, the left half from 9 down with no 0 leading,
// the largest digit left over in the middle, the half reversed after it.
package main

import "fmt"

func largestPalindromic(num string) string {
	var count [10]int64
	for i := 0; i < len(num); i++ {
		count[num[i]-'0']++
	}
	half := []byte{}
	for d := 9; d >= 0; d-- {
		if d == 0 && len(half) == 0 {
			break
		}
		for k := int64(0); k < count[d]/2; k++ {
			half = append(half, byte('0'+d))
		}
	}
	out := append([]byte{}, half...)
	for d := 9; d >= 0; d-- {
		if count[d]%2 == 1 {
			out = append(out, byte('0'+d))
			break
		}
	}
	if len(out) == 0 {
		return "0"
	}
	for i := len(half) - 1; i >= 0; i-- {
		out = append(out, half[i])
	}
	return string(out)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100 strings of 10^4 digits, string s's below 1 + s % 10, each a 0
	// with a chance of s % 7 in 10; each pass folds every answer's length
	// and middle digit
	seed := int64(2384)
	strings := make([]string, 100)
	for s := int64(0); s < 100; s++ {
		b := make([]byte, 10000)
		for i := range b {
			if nextRandom(&seed)%10 < s%7 {
				b[i] = '0'
			} else {
				b[i] = byte('0' + nextRandom(&seed)%(1+s%10))
			}
		}
		strings[s] = string(b)
	}
	check := int64(0)
	for p := int64(0); p < 200; p++ {
		for s := 0; s < 100; s++ {
			answer := largestPalindromic(strings[s])
			check = (check*31 + int64(len(answer)) + int64(answer[len(answer)/2]) + p) % 1000000007
		}
	}
	fmt.Printf("200 passes over 100 strings of 10^4 digits: checksum %d\n", check)
}
