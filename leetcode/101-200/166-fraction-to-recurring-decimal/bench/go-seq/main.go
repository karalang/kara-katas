package main

import "fmt"

func fracChecksum(num, den int64) int64 {
	rem := num % den
	var checksum int64 = 0
	if rem == 0 {
		return 0
	}
	pos := make(map[int64]int64)
	var count int64 = 0
	for rem != 0 {
		if _, ok := pos[rem]; ok {
			rem = 0 // cycle closed — stop
		} else {
			pos[rem] = count
			rem *= 10
			digit := rem / den
			checksum += digit
			rem %= den
			count++
		}
	}
	return checksum
}

func main() {
	var passes int64 = 500000
	var state int64 = 12345
	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		num := state % 1000000
		state = (state*1103515245 + 12345) & 2147483647
		den := 2 + (state % 1023)
		sink += fracChecksum(num, den)
	}
	fmt.Println(sink)
}
