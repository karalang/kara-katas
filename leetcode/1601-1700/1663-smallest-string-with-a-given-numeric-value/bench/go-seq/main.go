// LeetCode #1663 bench: the ★ arm, from the back.
//
// 400 problems with n = 10^5, LeetCode's largest, and k drawn from n to
// 26n, all drawn first; then each string is built and every letter of it
// folded into a checksum.
package main

import "fmt"

func getSmallestString(n, k int32) string {
	letters := make([]byte, n)
	for i := range letters {
		letters[i] = 'a'
	}
	left := int64(k) - int64(n)
	i := int64(n) - 1
	for left > 0 {
		more := min(left, 25)
		letters[i] += byte(more)
		left -= more
		i--
	}
	return string(letters)
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 400
	const n int64 = 100000
	seed = 1663
	ks := make([]int32, 0, count)
	for c := 0; c < count; c++ {
		r := nextRandom() * 32768
		r += nextRandom()
		ks = append(ks, int32(n+r%(25*n+1)))
	}
	var zs, check int64
	for _, k := range ks {
		s := getSmallestString(int32(n), k)
		for i := 0; i < len(s); i++ {
			b := s[i]
			if b == 'z' {
				zs++
			}
			check = (check*31 + int64(b)) % 1000000007
		}
	}
	fmt.Printf("%d problems with n = %d: %d z's, checksum %d\n", count, n, zs, check)
}
