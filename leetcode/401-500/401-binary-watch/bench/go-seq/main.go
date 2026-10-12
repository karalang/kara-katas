// Benchmark for #401: mirror of binary_watch.kara (try every time).
package main

import "fmt"

func ones(x int64) int64 {
	var count int64
	y := x
	for y > 0 {
		count += y % 2
		y = y / 2
	}
	return count
}

func readBinaryWatch(turnedOn int64) []string {
	var times []string
	for h := int64(0); h < 12; h++ {
		for m := int64(0); m < 60; m++ {
			if ones(h)+ones(m) == turnedOn {
				times = append(times, fmt.Sprintf("%d:%02d", h, m))
			}
		}
	}
	return times
}

func main() {
	calls := int64(50000)
	var timesTotal, chars int64
	for c := int64(0); c < calls; c++ {
		times := readBinaryWatch(c % 11)
		timesTotal += int64(len(times))
		for _, t := range times {
			chars += int64(len(t))
		}
	}
	fmt.Printf("%d calls: %d times, %d characters\n", calls, timesTotal, chars)
}
