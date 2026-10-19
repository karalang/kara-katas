// LeetCode 796 — Rotate String: the bench, in Go. Mirrors
// rotate_string.kara: goal is a rotation when it is as long as s and in
// s written twice, made fresh for each call.
package main

import (
	"fmt"
	"strings"
)

func rotateString(s, goal string) bool {
	return len(s) == len(goal) && strings.Contains(s+s, goal)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(796)
	ss := make([]string, 4096)
	goals := make([]string, 4096)
	for p := 0; p < 4096; p++ {
		letters := 1 + nextRandom(&seed)%4
		s := make([]byte, 100)
		for i := range s {
			s[i] = byte(97 + nextRandom(&seed)%letters)
		}
		kind := nextRandom(&seed) % 3
		goal := make([]byte, 100)
		if kind == 2 {
			for i := range goal {
				goal[i] = byte(97 + nextRandom(&seed)%letters)
			}
		} else {
			k := nextRandom(&seed) % 100
			change := int64(-1)
			if kind == 1 {
				change = nextRandom(&seed) % 100
			}
			for j := int64(0); j < 100; j++ {
				c := s[(j+k)%100]
				if j == change {
					goal[j] = byte(97 + (int64(c)-97+1)%letters)
				} else {
					goal[j] = c
				}
			}
		}
		ss[p] = string(s)
		goals[p] = string(goal)
	}
	rounds := 1500000
	var rotations, check int64
	for r := 0; r < rounds; r++ {
		if rotateString(ss[r%4096], goals[r%4096]) {
			rotations++
			check = (check*131 + int64(r%4096)) % 1000000007
		}
	}
	fmt.Printf("%d pairs: %d rotations, checksum %d\n", rounds, rotations, check)
}
