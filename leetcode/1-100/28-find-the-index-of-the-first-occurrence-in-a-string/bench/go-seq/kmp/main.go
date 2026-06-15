// LeetCode 28 — KMP strStr, Go seq mirror. Same adversarial input.
package main

import "fmt"

func buildLPS(pat []byte, m int64) []int64 {
	lps := make([]int64, m)
	var length int64
	i := int64(1)
	for i < m {
		if pat[i] == pat[length] {
			length++
			lps[i] = length
			i++
		} else if length > 0 {
			length = lps[length-1]
		} else {
			lps[i] = 0
			i++
		}
	}
	return lps
}

func strStr(haystack []byte, needle []byte) int64 {
	hn := int64(len(haystack))
	nn := int64(len(needle))
	if nn == 0 {
		return 0
	}
	if nn > hn {
		return -1
	}
	lps := buildLPS(needle, nn)
	var i, j int64
	for i < hn {
		if haystack[i] == needle[j] {
			i++
			j++
			if j == nn {
				return i - nn
			}
		} else if j > 0 {
			j = lps[j-1]
		} else {
			i++
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
