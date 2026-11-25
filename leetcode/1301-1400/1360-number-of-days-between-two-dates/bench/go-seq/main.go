// LeetCode #1360 bench -- Go: each date as its count of days from
// 1971-01-01, the answer the two counts' distance.
package main

import (
	"fmt"
	"strconv"
)

var lengths = [12]int64{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}

func isLeap(year int64) bool {
	return (year%4 == 0 && year%100 != 0) || year%400 == 0
}

func field(s string) int64 {
	v, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		panic(err)
	}
	return v
}

func daysFrom1971(date string) int64 {
	year := field(date[0:4])
	month := field(date[5:7])
	day := field(date[8:10])
	days := day - 1
	for y := int64(1971); y < year; y++ {
		if isLeap(y) {
			days += 366
		} else {
			days += 365
		}
	}
	for m := int64(1); m < month; m++ {
		days += lengths[m-1]
		if m == 2 && isLeap(year) {
			days++
		}
	}
	return days
}

func daysBetweenDates(date1, date2 string) int32 {
	d := daysFrom1971(date1) - daysFrom1971(date2)
	if d < 0 {
		d = -d
	}
	return int32(d)
}

var seed int64 = 1360

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomDate() string {
	year := 1971 + nextRandom()%130
	month := 1 + nextRandom()%12
	last := lengths[month-1]
	if month == 2 && isLeap(year) {
		last++
	}
	day := 1 + nextRandom()%last
	return fmt.Sprintf("%d-%02d-%02d", year, month, day)
}

func main() {
	// 1000 dates written once; then 3 * 10^5 questions, each pair of dates
	// drawn from the checksum so far, every answer folded into it
	dates := make([]string, 1000)
	for i := range dates {
		dates[i] = randomDate()
	}
	var check int64
	for r := int64(0); r < 300000; r++ {
		a := check % 1000
		b := (check/1000 + r) % 1000
		check = (check*31 + int64(daysBetweenDates(dates[a], dates[b])) + r) % 1000000007
	}
	fmt.Printf("300000 questions: checksum %d\n", check)
}
