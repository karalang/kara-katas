// LeetCode #1185: Day of the Week -- the ★ arm in Go: the days from
// 1 January 1971, a Friday, to the date, and that many days on from Friday.
package main

import (
	"fmt"
	"strings"
)

var names = []string{"Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"}
var monthDays = []int64{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}

func isLeap(year int64) bool {
	return (year%4 == 0 && year%100 != 0) || year%400 == 0
}

func dayOfTheWeek(day, month, year int64) string {
	days := int64(0)
	for y := int64(1971); y < year; y++ {
		if isLeap(y) {
			days += 366
		} else {
			days += 365
		}
	}
	for m := int64(1); m < month; m++ {
		days += monthDays[m-1]
	}
	if month > 2 && isLeap(year) {
		days++
	}
	days += day - 1
	return strings.Clone(names[days%7])
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1185)
	dates := [][3]int64{}
	for k := 0; k < 10000; k++ {
		year := 1971 + nextRandom(&seed)%130
		month := 1 + nextRandom(&seed)%12
		length := monthDays[month-1]
		if month == 2 && isLeap(year) {
			length = 29
		}
		day := 1 + nextRandom(&seed)%length
		dates = append(dates, [3]int64{day, month, year})
	}
	rounds := 100
	check := int64(0)
	for r := 0; r < rounds; r++ {
		for _, d := range dates {
			name := dayOfTheWeek(d[0], d[1], d[2])
			check = (check*131 + int64(len(name))*7 + int64(name[0]) + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 10000 dates: checksum %d\n", rounds, check)
}
