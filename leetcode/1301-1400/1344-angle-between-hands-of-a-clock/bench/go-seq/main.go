// LeetCode #1344 bench in Go: the ★ arm (the hour hand 30 degrees an hour
// plus half a degree a minute, the minute hand 6 a minute, and the smaller
// of the gap and 360 less it) on the same 3 * 10^7 times.
package main

import (
	"fmt"
	"math"
)

func angleClock(hour, minutes int32) float64 {
	hourHand := float64(hour%12)*30.0 + float64(minutes)*0.5
	minuteHand := float64(minutes) * 6.0
	gap := math.Abs(hourHand - minuteHand)
	return math.Min(gap, 360.0-gap)
}

func main() {
	var check int64
	for i := int64(0); i < 30000000; i++ {
		since := (i + check) % 720
		hour := since / 60
		if hour == 0 {
			hour = 12
		}
		a := angleClock(int32(hour), int32(since%60))
		check = (check*31 + int64(2.0*a)) % 1000000007
	}
	fmt.Printf("3 * 10^7 times: checksum %d\n", check)
}
