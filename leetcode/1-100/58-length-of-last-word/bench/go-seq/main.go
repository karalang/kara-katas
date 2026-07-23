package main

import "fmt"

func lastWordLen(buf []int64, end int64) int64 {
	i := end
	for i >= 0 && buf[i] == 32 {
		i--
	}
	var length int64 = 0
	for i >= 0 && buf[i] != 32 {
		length++
		i--
	}
	return length
}

func main() {
	var n int64 = 4000000
	var passes int64 = 6500000

	buf := make([]int64, 0, n)
	var state int64 = 12345
	for c := int64(0); c < n; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		r := state >> 16
		if r%100 < 18 {
			buf = append(buf, 32)
		} else {
			buf = append(buf, 65+r%26)
		}
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*97 + 13) % n
		if buf[idx] == 32 {
			buf[idx] = 65 + p%26
		} else {
			buf[idx] = 32
		}
		e := (p*89 + 41) % n
		sink += lastWordLen(buf, e)
	}
	fmt.Println(sink)
}
