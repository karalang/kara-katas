// Benchmark for #481: Go mirror of the ★ arm (the string read while it is
// written); see ../magical_string.kara.
package main

import "fmt"

func magicalString(n int64) int64 {
	s := []int64{1, 2, 2}
	read := 2
	for int64(len(s)) < n {
		next := 3 - s[len(s)-1]
		for k := int64(0); k < s[read]; k++ {
			s = append(s, next)
		}
		read++
	}
	var ones int64
	for i := int64(0); i < n; i++ {
		if s[i] == 1 {
			ones++
		}
	}
	return ones
}

func main() {
	var rounds int64 = 1000
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		ones := magicalString(100000 - r)
		total += ones
		checksum = (checksum*31 + ones) % 1000000007
	}
	fmt.Printf("%d rounds of n = 99001 to 100000: 1s add up to %d, checksum %d\n", rounds, total, checksum)
}
