package main

import "fmt"

const W int64 = 96

func addPopcount(bits []int64, offA, offB int64) int64 {
	var carry int64 = 0
	var pop int64 = 0
	for k := W - 1; k >= 0; k-- {
		s := carry + bits[offA+k] + bits[offB+k]
		pop += s & 1
		carry = s >> 1
	}
	pop += carry
	return pop
}

func main() {
	var bn int64 = 2000000
	var passes int64 = 2600000

	bits := make([]int64, 0, bn)
	var state int64 = 12345
	for c := int64(0); c < bn; c++ {
		state = (state*1103515245 + 12345) & 2147483647
		bits = append(bits, (state>>16)&1)
	}

	span := bn - W
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*101 + 7) % bn
		bits[idx] = 1 - bits[idx]
		offA := (p * 37) % span
		offB := (p*53 + 17) % span
		sink += addPopcount(bits, offA, offB)
	}
	fmt.Println(sink)
}
