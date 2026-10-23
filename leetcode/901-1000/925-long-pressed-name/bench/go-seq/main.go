// LeetCode #925: Long Pressed Name -- bench: two pointers.
// Mirrors is_long_pressed_name.kara.
package main

import "fmt"

func isLongPressedName(name, typed string) bool {
	i := 0
	for j := 0; j < len(typed); j++ {
		if i < len(name) && name[i] == typed[j] {
			i++
		} else if j > 0 && typed[j] == typed[j-1] {
			continue
		} else {
			return false
		}
	}
	return i == len(name)
}

var seed int64 = 925

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count = 150, 1000
	// count names of 400 letters from "abc", each typed with about one key
	// in four held down for up to three more presses, and every third one
	// mistyped once
	names := make([]string, count)
	typings := make([]string, count)
	for p := 0; p < count; p++ {
		var name, typed []byte
		for k := 0; k < 400; k++ {
			c := byte('a' + nextRandom()%3)
			name = append(name, c)
			var extra int64
			if nextRandom()%4 == 0 {
				extra = 1 + nextRandom()%3
			}
			for e := int64(0); e < 1+extra; e++ {
				typed = append(typed, c)
			}
		}
		if p%3 == 0 {
			at := nextRandom() % int64(len(typed))
			typed[at] = byte('a' + nextRandom()%3)
		}
		names[p] = string(name)
		typings[p] = string(typed)
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every pair, starting from a different one
		for i := 0; i < count; i++ {
			p := (r + i) % count
			if isLongPressedName(names[p], typings[p]) {
				yes++
				check = (check*1000003 + int64(p) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d names of 400 letters: %d long pressed, checksum %d\n", rounds, count, yes, check)
}
