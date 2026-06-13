// LeetCode 28 — brute-force sliding-window strStr, Go seq mirror.
package main

import "fmt"

func strStr(haystack []byte, needle []byte) int64 {
	hn := int64(len(haystack))
	nn := int64(len(needle))
	if nn == 0 {
		return 0
	}
	if nn > hn {
		return -1
	}
	for i := int64(0); i <= hn-nn; i++ {
		j := int64(0)
		for j < nn && haystack[i+j] == needle[j] {
			j++
		}
		if j == nn {
			return i
		}
	}
	return -1
}

func main() {
	const N = 2_000_000
	const M = 16

	haystack := make([]byte, N)
	for i := range haystack {
		haystack[i] = 'a'
	}
	haystack[N-1] = 'b'
	needle := make([]byte, M)
	for i := range needle {
		needle[i] = 'a'
	}
	needle[M-1] = 'b'

	var total int64
	for iter := 0; iter < 100; iter++ {
		total += strStr(haystack, needle)
	}
	fmt.Println(total)
}
