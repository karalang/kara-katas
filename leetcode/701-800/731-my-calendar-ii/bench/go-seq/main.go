// LeetCode #731: My Calendar II -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings and
// the stretches two of them cover, and refuse a booking that meets one
// of those stretches.
package main

import "fmt"

type booking struct{ start, end int64 }

type MyCalendarTwo struct{ booked, doubled []booking }

func (c *MyCalendarTwo) Book(start, end int64) bool {
	for _, d := range c.doubled {
		if start < d.end && d.start < end {
			return false
		}
	}
	for _, b := range c.booked {
		if start < b.end && b.start < end {
			lo, hi := b.start, b.end
			if start > lo {
				lo = start
			}
			if end < hi {
				hi = end
			}
			c.doubled = append(c.doubled, booking{lo, hi})
		}
	}
	c.booked = append(c.booked, booking{start, end})
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(731)
	lists := make([][]booking, 0, 20)
	for d := 0; d < 20; d++ {
		bookings := make([]booking, 0, 1000)
		for i := 0; i < 1000; i++ {
			s := (nextRandom(&seed)*32768 + nextRandom(&seed)) % 996999000
			length := 1 + (nextRandom(&seed)*32768+nextRandom(&seed))%3000000
			bookings = append(bookings, booking{s, s + length})
		}
		lists = append(lists, bookings)
	}
	accepted := 0
	for round := int64(0); round < 80; round++ {
		for d := 0; d < 20; d++ {
			cal := MyCalendarTwo{}
			for _, b := range lists[d] {
				if cal.Book(b.start+round, b.end+round) {
					accepted++
				}
			}
		}
	}
	fmt.Printf("80 rounds of 20 lists of 1000 bookings: %d accepted\n", accepted)
}
