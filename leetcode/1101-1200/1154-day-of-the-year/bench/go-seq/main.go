// LeetCode #1154 bench -- mirrors day_of_year.kara: the same dates, the
// same passes, the ★ arm's table.
package main

import (
	"fmt"
	"strconv"
)

var before = [12]int64{0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334}

func isLeap(year int64) bool {
	return year%4 == 0 && (year%100 != 0 || year%400 == 0)
}

func parse(s string) int64 {
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		panic(err)
	}
	return n
}

func dayOfYear(date string) int64 {
	year := parse(date[0:4])
	month := parse(date[5:7])
	day := parse(date[8:10])
	var leapDay int64
	if month > 2 && isLeap(year) {
		leapDay = 1
	}
	return before[month-1] + day + leapDay
}

func daysIn(year, month int64) int64 {
	if month == 2 {
		if year%400 == 0 || (year%4 == 0 && year%100 != 0) {
			return 29
		}
		return 28
	}
	return 31 - (month-1)%7%2
}

func main() {
	passes := int64(1000)
	dates := []string{}
	for year := int64(1900); year < 2020; year++ {
		for month := int64(1); month < 13; month++ {
			for day := int64(1); day < daysIn(year, month)+1; day++ {
				dates = append(dates, fmt.Sprintf("%d-%02d-%02d", year, month, day))
			}
		}
	}
	var total, check int64
	for p := int64(0); p < passes; p++ {
		for _, date := range dates {
			n := dayOfYear(date)
			total += n
			check = (check*31 + n + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over %d dates: total %d, checksum %d\n", passes, len(dates), total, check)
}
