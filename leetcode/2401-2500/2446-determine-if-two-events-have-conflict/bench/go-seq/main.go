// LeetCode #2446: Determine if Two Events Have Conflict -- the bench, the
// ★ arm: the four `HH:MM` strings compared as text.
package main

import "fmt"

func haveConflict(event1, event2 []string) bool {
	return event1[0] <= event2[1] && event2[0] <= event1[1]
}

var seed int64 = 2446

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func clock(minute int64) string {
	return fmt.Sprintf("%02d:%02d", minute/60, minute%60)
}

func main() {
	const n = 100000
	var events [][]string
	for i := 0; i < n; i++ {
		a := nextRandom() % 1440
		b := nextRandom() % 1440
		events = append(events, []string{clock(min(a, b)), clock(max(a, b))})
	}
	var check int64
	for p := int64(0); p < 300; p++ {
		for i := int64(0); i < n; i++ {
			j := (7*i + p + 1) % n
			var answer int64
			if haveConflict(events[i], events[j]) {
				answer = 1
			}
			check = (check*31 + answer + p) % 1000000007
		}
	}
	fmt.Printf("300 passes over 10^5 events: checksum %d\n", check)
}
