// Benchmark for #359 -- mirror of logger.kara.
package main

import "fmt"

type logger struct{ nextOK map[string]int64 }

func (l *logger) shouldPrintMessage(timestamp int64, message string) bool {
	if t, ok := l.nextOK[message]; ok && timestamp < t {
		return false
	}
	l.nextOK[message] = timestamp + 10
	return true
}

func main() {
	var seed int64 = 359
	l := &logger{nextOK: map[string]int64{}}
	var t int64
	printed := 0
	var checksum int64
	for i := 0; i < 1000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		if (seed/65536)%8 == 0 {
			t++
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		id := (seed / 65536) % 100
		ok := l.shouldPrintMessage(t, fmt.Sprintf("msg%d", id))
		if ok {
			printed++
		}
		if ok {
			checksum = (checksum*3 + 1) % 1000000007
		} else {
			checksum = (checksum*3 + 2) % 1000000007
		}
	}
	fmt.Printf("%d of 1000000 calls printed, checksum %d\n", printed, checksum)
}
