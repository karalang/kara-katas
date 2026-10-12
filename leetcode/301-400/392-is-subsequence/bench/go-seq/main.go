// Benchmark for #392: mirror of is_subsequence.kara (two pointers).
package main

import "fmt"

func isSubsequence(s, t string) bool {
	i := 0
	for k := 0; k < len(t); k++ {
		if i < len(s) && s[i] == t[k] {
			i++
		}
	}
	return i == len(s)
}

var seed int64 = 392

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	hi := step()
	return hi*32768 + step()
}

func main() {
	buf := make([]byte, 1000000)
	for i := range buf {
		buf[i] = byte(step()%26 + 97)
	}
	pool := string(buf)
	yes := 0
	var checksum int64
	for k := 0; k < 20000; k++ {
		a := big() % (1000000 - 100)
		length := step() % 10001
		b := big() % (1000000 - length)
		r := isSubsequence(pool[a:a+100], pool[b:b+length])
		if r {
			yes++
			checksum = (checksum*3 + 1) % 1000000007
		} else {
			checksum = (checksum*3 + 2) % 1000000007
		}
	}
	fmt.Printf("20000 pairs: %d subsequences, checksum %d\n", yes, checksum)
}
