// LeetCode #1047: Remove All Adjacent Duplicates In String -- Go mirror of
// bench/remove_dups.kara: a []rune stack, turned into a string.
package main

import "fmt"

var seed int64 = 1047

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func removeDuplicates(s string) string {
	stack := []rune{}
	for _, c := range s {
		if len(stack) > 0 && stack[len(stack)-1] == c {
			stack = stack[:len(stack)-1]
		} else {
			stack = append(stack, c)
		}
	}
	return string(stack)
}

func main() {
	count, n, rounds := 100, 200000, 10
	strings := make([]string, 0, count)
	for k := 0; k < count; k++ {
		b := make([]byte, n)
		for i := range b {
			b[i] = byte('a' + nextRandom()%4)
		}
		strings = append(strings, string(b))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strings {
			answer := removeDuplicates(s)
			var last int64
			if len(answer) > 0 {
				last = int64(answer[len(answer)-1])
			}
			total += int64(len(answer))
			check = (check*131 + int64(len(answer)) + last) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d letters, %d rounds: total length %d, checksum %d\n", count, n, rounds, total, check)
}
