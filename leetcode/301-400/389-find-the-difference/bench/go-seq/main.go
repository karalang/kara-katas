// Benchmark for #389: mirror of find_the_difference.kara (XOR of every byte).
package main

import "fmt"

func findTheDifference(s, t string) byte {
	var x byte
	for i := 0; i < len(s); i++ {
		x ^= s[i]
	}
	for i := 0; i < len(t); i++ {
		x ^= t[i]
	}
	return x
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(389)
	buf := make([]byte, 1000000)
	for i := range buf {
		buf[i] = byte(step(&seed)%26 + 97)
	}
	pool := string(buf)
	right := 0
	var checksum int64
	for q := 0; q < 8000000; q++ {
		n := step(&seed) % 1001
		a := step(&seed) % (1000000 - n - 1)
		c := findTheDifference(pool[a:a+n], pool[a:a+n+1])
		if c == pool[a+n] {
			right++
		}
		checksum = (checksum*31 + int64(c)) % 1000000007
	}
	fmt.Printf("8000000 pairs, %d right, checksum %d\n", right, checksum)
}
