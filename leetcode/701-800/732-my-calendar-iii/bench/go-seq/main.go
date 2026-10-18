// LeetCode #732: My Calendar III -- starts and ends, merged.
// Benchmark mirror of the Kara star arm: keep the starts and the ends
// in two sorted slices, each put in its place by binary search, and
// sweep both together for the most bookings at once.
package main

import "fmt"

type MyCalendarThree struct{ starts, ends []int64 }

func place(v []int64, x int64) []int64 {
	lo, hi := 0, len(v)
	for lo < hi {
		mid := (lo + hi) / 2
		if v[mid] <= x {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	v = append(v, 0)
	copy(v[lo+1:], v[lo:])
	v[lo] = x
	return v
}

func (c *MyCalendarThree) Book(start, end int64) int64 {
	c.starts = place(c.starts, start)
	c.ends = place(c.ends, end)
	n := len(c.starts)
	i, j := 0, 0
	var now, most int64
	for i < n {
		if c.ends[j] <= c.starts[i] {
			now--
			j++
		} else {
			now++
			i++
			if now > most {
				most = now
			}
		}
	}
	return most
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type booking struct{ start, end int64 }

func main() {
	seed := int64(732)
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
	var sum int64
	for round := int64(0); round < 40; round++ {
		for d := 0; d < 20; d++ {
			cal := MyCalendarThree{}
			for _, b := range lists[d] {
				sum += cal.Book(b.start+round, b.end+round)
			}
		}
	}
	fmt.Printf("40 rounds of 20 lists of 1000 bookings: answers sum %d\n", sum)
}
