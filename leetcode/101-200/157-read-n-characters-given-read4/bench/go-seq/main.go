package main

import "fmt"

type Reader struct {
	pos int64
	chk int64
}

func read4(src []int64, m int64, rd *Reader) int64 {
	var cnt int64 = 0
	for cnt < 4 && rd.pos < m {
		rd.pos++
		cnt++
	}
	return cnt
}

func readN(src []int64, m int64, rd *Reader, want int64) int64 {
	var total int64 = 0
	acc := rd.chk
	eof := false
	for total < want && !eof {
		start := rd.pos
		cnt := read4(src, m, rd)
		if cnt == 0 {
			eof = true
		} else {
			var take int64
			if total+cnt <= want {
				take = cnt
			} else {
				take = want - total
			}
			for k := int64(0); k < take; k++ {
				acc = (acc*1103515245 + src[start+k] + 1) & 2147483647
			}
			total += take
		}
	}
	rd.chk = acc
	return total
}

func main() {
	var size int64 = 50000
	var want int64 = 7
	var passes int64 = 3200

	src := make([]int64, size)
	var state int64 = 12345
	for c := int64(0); c < size; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		src[c] = state % 26
	}

	rd := &Reader{pos: 0, chk: 0}
	for pass := int64(0); pass < passes; pass++ {
		idx := (pass*131 + 7) % size
		src[idx] = (src[idx] + 1) % 26
		rd.pos = 0
		cont := true
		for cont {
			got := readN(src, size, rd, want)
			if got == 0 {
				cont = false
			}
		}
	}
	fmt.Println(rd.chk)
}
