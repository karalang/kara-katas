// LeetCode #1312 bench, Go: the ★ arm (the interval costs kept in one row)
// on the same 20 strings and 50 passes.
package main

import "fmt"

func minInsertions(s string) int64 {
	n := len(s)
	row := make([]int64, n)
	for i := n - 1; i >= 0; i-- {
		var inside int64
		for j := i + 1; j < n; j++ {
			keep := row[j]
			if s[i] == s[j] {
				row[j] = inside
			} else {
				row[j] = 1 + min(keep, row[j-1])
			}
			inside = keep
		}
	}
	return row[n-1]
}

var seed int64 = 1312

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	const n = 500
	strings := make([][]byte, 20)
	for g := 0; g < 20; g++ {
		k := int64(26)
		if g%3 == 0 {
			k = 2
		} else if g%3 == 1 {
			k = 4
		}
		chars := make([]byte, n)
		for i := range chars {
			chars[i] = letters[nextRandom()%k]
		}
		strings[g] = chars
	}
	var check int64
	for pass := int64(0); pass < 50; pass++ {
		for g := 0; g < 20; g++ {
			k := int64(26)
			if g%3 == 0 {
				k = 2
			} else if g%3 == 1 {
				k = 4
			}
			strings[g][check%n] = letters[(check/7)%k]
			got := minInsertions(string(strings[g]))
			check = (check*31 + got + pass) % 1000000007
		}
	}
	fmt.Printf("50 passes over 20 strings of 500: checksum %d\n", check)
}
