// Benchmark mirror of ransom_note.kara (#383).
package main

import "fmt"

func canConstruct(note, magazine string) bool {
	var count [26]int64
	for i := 0; i < len(magazine); i++ {
		count[magazine[i]-'a']++
	}
	for i := 0; i < len(note); i++ {
		k := note[i] - 'a'
		count[k]--
		if count[k] < 0 {
			return false
		}
	}
	return true
}

func main() {
	seed := int64(383)
	buf := make([]byte, 1000000)
	for i := range buf {
		seed = (seed*1103515245 + 12345) % 2147483648
		buf[i] = byte((seed/65536)%26 + 97)
	}
	pool := string(buf)
	yes := 0
	checksum := int64(0)
	for q := 0; q < 10000; q++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		n := 30000 + (seed/64)%40000
		seed = (seed*1103515245 + 12345) % 2147483648
		m := 40000 + (seed/64)%40000
		seed = (seed*1103515245 + 12345) % 2147483648
		a := (seed / 64) % (1000000 - n)
		seed = (seed*1103515245 + 12345) % 2147483648
		b := (seed / 64) % (1000000 - m)
		ok := canConstruct(pool[a:a+n], pool[b:b+m])
		if ok {
			yes++
		}
		v := int64(2)
		if ok {
			v = 1
		}
		checksum = (checksum*3 + v) % 1000000007
	}
	fmt.Printf("%d of 10000 can be built, checksum %d\n", yes, checksum)
}
