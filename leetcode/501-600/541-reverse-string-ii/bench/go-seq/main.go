// Benchmark for #541: Go mirror of the ★ arm (two pointers over the
// characters); see ../reverse_str.kara.
package main

import "fmt"

func reverseStr(s string, k int) string {
	chars := []rune(s)
	n := len(chars)
	for start := 0; start < n; start += 2 * k {
		i, j := start, min(start+k, n)-1
		for i < j {
			chars[i], chars[j] = chars[j], chars[i]
			i++
			j--
		}
	}
	return string(chars)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 200 random words of 10,000 letters (the problem's longest) built
	// once. Then 100 times over every word is answered with a k from 1
	// to 500 picked by the round and the word, and one letter of the
	// answer, picked the same way, goes into the checksum.
	words := 200
	seed := int64(541)
	all := make([]string, words)
	for t := range all {
		b := make([]byte, 10000)
		for i := range b {
			b[i] = byte('a' + nextRandom(&seed)%26)
		}
		all[t] = string(b)
	}
	total := 0
	var checksum int64
	for r := 0; r < 100; r++ {
		for t := 0; t < words; t++ {
			k := 1 + (r*37+t*11)%500
			answer := reverseStr(all[t], k)
			letter := int64(answer[(r*7+t*13)%10000])
			total += len(answer)
			checksum = (checksum*31 + letter) % 1000000007
		}
	}
	fmt.Printf("%d words, 100 times each: %d letters, checksum %d\n", words, total, checksum)
}
