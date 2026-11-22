// LeetCode #2716: Minimize String Length -- the bench (minimize.kara in
// Go): the distinct letters of each string counted by a
// `map[rune]struct{}`.
package main

import "fmt"

func minimizedStringLength(s string) int64 {
	seen := make(map[rune]struct{})
	for _, c := range s {
		seen[c] = struct{}{}
	}
	return int64(len(seen))
}

var seed int64 = 2716

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 100000, 10
	strings := make([]string, 0, count)
	for k := 0; k < count; k++ {
		letters := nextRandom()%26 + 1
		b := make([]byte, 100)
		for i := range b {
			b[i] = byte('a' + nextRandom()%letters)
		}
		strings = append(strings, string(b))
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			length := minimizedStringLength(s)
			sum += length
			check = (check*31 + length + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d strings of 100 letters, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}
