// LeetCode #1507: Reformat Date -- the bench: 100000 dates built once,
// then each reformatted ten times by the ★ arm.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

var months = []string{"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}

func reformatDate(date string) string {
	parts := strings.Split(date, " ")
	end := 0
	for end < len(parts[0]) && parts[0][end] >= '0' && parts[0][end] <= '9' {
		end++
	}
	day, _ := strconv.Atoi(parts[0][:end])
	month := 0
	for m, name := range months {
		if name == parts[1] {
			month = m + 1
			break
		}
	}
	return fmt.Sprintf("%s-%02d-%02d", parts[2], month, day)
}

func suffix(day int64) string {
	switch day {
	case 1, 21, 31:
		return "st"
	case 2, 22:
		return "nd"
	case 3, 23:
		return "rd"
	}
	return "th"
}

func daysIn(month, year int64) int64 {
	days := [12]int64{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
	leap := year%4 == 0 && (year%100 != 0 || year%400 == 0)
	if month == 1 && leap {
		return 29
	}
	return days[month]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1507)
	dates := make([]string, 0, 100000)
	for i := 0; i < 100000; i++ {
		year := 1900 + nextRandom(&seed)%201
		month := nextRandom(&seed) % 12
		day := 1 + nextRandom(&seed)%daysIn(month, year)
		dates = append(dates, fmt.Sprintf("%d%s %s %d", day, suffix(day), months[month], year))
	}
	var check int64
	for r := 0; r < 10; r++ {
		for _, date := range dates {
			out := reformatDate(date)
			for i := 0; i < len(out); i++ {
				check = (check*31 + int64(out[i]) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("1000000 dates reformatted, 100000 built once: checksum %d\n", check)
}
