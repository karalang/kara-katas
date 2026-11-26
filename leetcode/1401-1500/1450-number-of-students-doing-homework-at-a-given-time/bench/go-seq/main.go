// LeetCode #1450 Number of Students Doing Homework at a Given Time: the
// bench, a mirror of busy_student.kara.
package main

import "fmt"

// each student's start and end side by side, counted when the query falls
// between them
func busyStudent(startTime, endTime []int32, queryTime int32) int32 {
	var busy int32
	for i, s := range startTime {
		if s <= queryTime && queryTime <= endTime[i] {
			busy++
		}
	}
	return busy
}

func main() {
	// 3000 classes of 100 students, the constraints' most, each from a
	// start to an end drawn from 1 to 1000, each class asked at every time
	// from 1 to 1000, the counts folded to a checksum
	var seed int64 = 1450
	var check int64 = 0
	for r := 0; r < 3000; r++ {
		startTime := make([]int32, 0, 100)
		endTime := make([]int32, 0, 100)
		for i := 0; i < 100; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			a := 1 + seed/65536%1000
			seed = (seed*1103515245 + 12345) % 2147483648
			b := 1 + seed/65536%1000
			startTime = append(startTime, int32(min(a, b)))
			endTime = append(endTime, int32(max(a, b)))
		}
		for q := int32(1); q <= 1000; q++ {
			check = (check*131 + int64(busyStudent(startTime, endTime, q))) % 1000000007
		}
	}
	fmt.Printf("3000 classes asked 1000 times: checksum %d\n", check)
}
