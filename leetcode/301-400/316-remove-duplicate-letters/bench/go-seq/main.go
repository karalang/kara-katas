// Benchmark lane for LeetCode 316 — Go mirror of bench/remove_duplicate_letters.kara.
// Generate N drifting letters once, then PASSES monotone-stack passes (record
// each letter's last occurrence, then skip placed letters and pop larger tops
// that still have a later copy), each after overwriting one position chosen
// from the checksum.
package main

import "fmt"

const (
	N      = 4000000
	PASSES = 100
	MASK   = 1073741823
)

func lcg(s int64) int64 {
	return (s*1103515245 + 12345) & 0x7fffffff
}

func removeDuplicateLetters(bs []byte) []byte {
	n := len(bs)
	var last [26]int64
	for k := 0; k < 26; k++ {
		last[k] = -1
	}
	for i := 0; i < n; i++ {
		last[bs[i]-'a'] = int64(i)
	}
	var onStack [26]bool
	stack := make([]byte, 0, 26)
	for i := 0; i < n; i++ {
		c := bs[i]
		ci := c - 'a'
		if onStack[ci] {
			continue
		}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			if top > c && last[top-'a'] > int64(i) {
				stack = stack[:len(stack)-1]
				onStack[top-'a'] = false
			} else {
				break
			}
		}
		stack = append(stack, c)
		onStack[ci] = true
	}
	return stack
}

func main() {
	var seed int64 = 316
	text := make([]byte, 0, N)
	var cur int64 = 25
	for i := 0; i < N; i++ {
		seed = lcg(seed)
		r := seed / 65536
		if r%4 != 0 {
			cur--
			if cur < 0 {
				cur = 25
			}
		} else {
			cur = r % 26
		}
		text = append(text, byte(cur)+'a')
	}

	var checksum int64 = 0
	for pass := 0; pass < PASSES; pass++ {
		i := checksum % N
		letter := byte((checksum*7 + 13) % 26)
		saved := text[i]
		text[i] = letter + 'a'
		out := removeDuplicateLetters(text)
		var fold int64 = 0
		for _, b := range out {
			fold = (fold*131 + int64(b)) & MASK
		}
		checksum = (checksum*31 + fold + int64(len(out))) & MASK
		text[i] = saved
	}
	fmt.Printf("checksum %d\n", checksum)
}
