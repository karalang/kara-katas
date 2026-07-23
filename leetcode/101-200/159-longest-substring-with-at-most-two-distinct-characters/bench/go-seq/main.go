package main

import "fmt"

func longest(buf []int64, lo, hi, alphabet int64) int64 {
	var counts [8]int64
	for a := int64(0); a < alphabet; a++ {
		counts[a] = 0
	}
	var distinct int64 = 0
	left := lo
	var best int64 = 0
	for right := lo; right < hi; right++ {
		c := buf[right]
		if counts[c] == 0 {
			distinct++
		}
		counts[c]++
		for distinct > 2 {
			lc := buf[left]
			counts[lc]--
			if counts[lc] == 0 {
				distinct--
			}
			left++
		}
		w := right - left + 1
		if w > best {
			best = w
		}
	}
	return best
}

func main() {
	var size int64 = 20000
	var alphabet int64 = 8
	var width int64 = 96
	var reps int64 = 100

	buf := make([]int64, size)
	var state int64 = 12345
	for c := int64(0); c < size; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		buf[c] = state % alphabet
	}

	ranges := size - width
	var sink int64 = 0
	for rep := int64(0); rep < reps; rep++ {
		idx := (rep*131 + 7) % size
		buf[idx] = (buf[idx] + 1) % alphabet
		for start := int64(0); start < ranges; start++ {
			sink += longest(buf, start, start+width, alphabet)
		}
	}
	fmt.Println(sink)
}
