// LeetCode #2124: Check if All A's Appears Before All B's -- the
// benchmark, the same algorithm as abba.kara: the answer is that "ba"
// does not occur.

package main

import (
	"fmt"
	"strings"
)

func checkString(s string) bool {
	return !strings.Contains(s, "ba")
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2124)
	strs := make([]string, 0, 100000)
	for n := 0; n < 100000; n++ {
		split := nextRandom(&seed) % 101
		letters := make([]byte, 100)
		for i := range letters {
			if int64(i) < split {
				letters[i] = 'a'
			} else {
				letters[i] = 'b'
			}
		}
		if nextRandom(&seed)%4 == 0 {
			at := nextRandom(&seed) % 100
			if letters[at] == 'a' {
				letters[at] = 'b'
			} else {
				letters[at] = 'a'
			}
		}
		strs = append(strs, string(letters))
	}
	var ordered, check int64
	for round := 0; round < 50; round++ {
		k := round * 7919 % 100000
		at := round * 31 % 100
		letters := []byte(strs[k])
		if letters[at] == 'a' {
			letters[at] = 'b'
		} else {
			letters[at] = 'a'
		}
		strs[k] = string(letters)
		for i := range strs {
			if checkString(strs[i]) {
				ordered++
				check = (check*31 + int64(i)) % 1000000007
			}
		}
	}
	fmt.Printf("5000000 checks: %d in order, checksum %d\n", ordered, check)
}
