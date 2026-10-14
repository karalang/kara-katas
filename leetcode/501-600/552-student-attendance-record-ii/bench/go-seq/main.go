// Benchmark for #552: Go mirror of the ★ arm (six counters, rolled); see
// ../student_attendance_record_ii.kara.
package main

import "fmt"

func checkRecord(n int64) int64 {
	const m = 1000000007
	count := []int64{1, 0, 0, 0, 0, 0}
	for d := int64(0); d < n; d++ {
		next := make([]int64, 6)
		for a := 0; a < 2; a++ {
			for l := 0; l < 3; l++ {
				c := count[a*3+l]
				if c == 0 {
					continue
				}
				next[a*3] = (next[a*3] + c) % m
				if a == 0 {
					next[3] = (next[3] + c) % m
				}
				if l < 2 {
					next[a*3+l+1] = (next[a*3+l+1] + c) % m
				}
			}
		}
		count = next
	}
	var total int64
	for _, c := range count {
		total = (total + c) % m
	}
	return total
}

func main() {
	var checksum, days int64
	for k := int64(0); k < 100; k++ {
		n := 100000 - (k*997)%1000
		days += n
		checksum = (checksum*31 + checkRecord(n)) % 1000000007
	}
	fmt.Printf("100 lengths, %d days: checksum %d\n", days, checksum)
}
