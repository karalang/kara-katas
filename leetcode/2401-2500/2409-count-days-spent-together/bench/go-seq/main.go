// LeetCode #2409: Count Days Spent Together -- the bench, the ★ arm in Go:
// each "MM-DD" read from its bytes into a day of the year, the shared stay
// from the later arrival to the earlier departure.

package main

import "fmt"

var seed int64 = 2409
var before = [12]int64{0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334}

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func dayOfYear(date string) int64 {
	month := int64(date[0]-'0')*10 + int64(date[1]-'0')
	day := int64(date[3]-'0')*10 + int64(date[4]-'0')
	return before[month-1] + day
}

func countDaysTogether(arriveAlice, leaveAlice, arriveBob, leaveBob string) int64 {
	first := max(dayOfYear(arriveAlice), dayOfYear(arriveBob))
	last := min(dayOfYear(leaveAlice), dayOfYear(leaveBob))
	return max(last-first+1, 0)
}

func main() {
	lengths := []int{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
	var names []string
	for m := 0; m < 12; m++ {
		for d := 0; d < lengths[m]; d++ {
			names = append(names, fmt.Sprintf("%02d-%02d", m+1, d+1))
		}
	}
	stays := make([][4]int64, 100000)
	for i := range stays {
		a, b := nextRandom()%365, nextRandom()%365
		c, d := nextRandom()%365, nextRandom()%365
		stays[i] = [4]int64{min(a, b), max(a, b), min(c, d), max(c, d)}
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for _, s := range stays {
			check = (check*31 + countDaysTogether(names[s[0]], names[s[1]], names[s[2]], names[s[3]]) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10^5 pairs of stays: checksum %d\n", check)
}
