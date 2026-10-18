// LeetCode #729: My Calendar I -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings in
// a list and accept a new one only if it overlaps none of them.
package main

import "fmt"

type booking struct{ start, end int64 }

type MyCalendar struct{ booked []booking }

func (c *MyCalendar) Book(start, end int64) bool {
	for _, b := range c.booked {
		if start < b.end && b.start < end {
			return false
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
	seed := int64(729)
	lists := make([][]booking, 0, 20)
	for d := 0; d < 20; d++ {
		bookings := make([]booking, 0, 1000)
		for i := 0; i < 1000; i++ {
			s := (nextRandom(&seed)*32768 + nextRandom(&seed)) % 998999000
			length := 1 + (nextRandom(&seed)*32768+nextRandom(&seed))%1000000
			bookings = append(bookings, booking{s, s + length})
		}
		lists = append(lists, bookings)
	}
	accepted := 0
	for round := int64(0); round < 80; round++ {
		for d := 0; d < 20; d++ {
			cal := MyCalendar{}
			for _, b := range lists[d] {
				if cal.Book(b.start+round, b.end+round) {
					accepted++
				}
			}
		}
	}
	fmt.Printf("80 rounds of 20 lists of 1000 bookings: %d accepted\n", accepted)
}
