// Benchmark for #551: Go mirror of the ★ arm (one pass, two counters);
// see ../student_attendance_record_i.kara.
package main

import (
	"fmt"
	"strings"
)

func checkRecord(s string) bool {
	absences, lates := 0, 0
	for _, c := range s {
		if c == 'L' {
			lates++
			if lates == 3 {
				return false
			}
		} else {
			lates = 0
			if c == 'A' {
				absences++
				if absences == 2 {
					return false
				}
			}
		}
	}
	return true
}

var seed int64 = 551

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 1000
	records := make([]string, count)
	for g := 0; g < count; g++ {
		var b strings.Builder
		for d := 0; d < 1000; d++ {
			r := nextRandom() % 2000
			if r < 1 {
				b.WriteByte('A')
			} else if r < 101 {
				b.WriteByte('L')
			} else {
				b.WriteByte('P')
			}
		}
		records[g] = b.String()
	}
	var fine, checksum int64
	for round := 0; round < 300; round++ {
		for g := 0; g < count; g++ {
			var bit int64
			if checkRecord(records[(round*7+g)%count]) {
				bit = 1
			}
			fine += bit
			checksum = (checksum*31 + bit + int64(g)) % 1000000007
		}
	}
	fmt.Printf("%d records, 300 rounds each: %d fine, checksum %d\n", count, fine, checksum)
}
