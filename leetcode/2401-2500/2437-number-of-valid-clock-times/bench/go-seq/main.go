// LeetCode #2437: Number of Valid Clock Times -- the bench, the ★ arm:
// the hours that fit the first two characters times the minutes that
// fit the last two.
package main

import "fmt"

func fits(pattern string, value int64) bool {
	tens := byte('0' + value/10)
	units := byte('0' + value%10)
	return (pattern[0] == '?' || pattern[0] == tens) && (pattern[1] == '?' || pattern[1] == units)
}

func countTime(time string) int64 {
	var hours, minutes int64
	for h := int64(0); h < 24; h++ {
		if fits(time[0:2], h) {
			hours++
		}
	}
	for m := int64(0); m < 60; m++ {
		if fits(time[3:5], m) {
			minutes++
		}
	}
	return hours * minutes
}

func main() {
	var times []string
	for at := 0; at < 1440; at++ {
		for mask := 0; mask < 16; mask++ {
			shown := fmt.Sprintf("%02d:%02d", at/60, at%60)
			out := make([]byte, 0, 5)
			digit := 0
			for i := 0; i < len(shown); i++ {
				c := shown[i]
				if c == ':' {
					out = append(out, c)
				} else {
					if (mask>>digit)&1 == 1 {
						out = append(out, '?')
					} else {
						out = append(out, c)
					}
					digit++
				}
			}
			times = append(times, string(out))
		}
	}
	var check int64
	n := int64(len(times))
	for p := int64(0); p < 120; p++ {
		for i := int64(0); i < n; i++ {
			check = (check*31 + countTime(times[(i*7+p)%n]) + p) % 1000000007
		}
	}
	fmt.Printf("120 passes over 23040 patterns: checksum %d\n", check)
}
