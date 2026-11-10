// LeetCode #1109: Corporate Flight Bookings -- the bench in Go: the ★ arm
// (a difference array and a running total) over 16 problems of 2 * 10^4
// flights and 2 * 10^4 bookings, each round changing one booking in every
// problem and solving it again.
package main

import "fmt"

func corpFlightBookings(bookings [][]int64, n int64) []int64 {
	change := make([]int64, n+1)
	for _, b := range bookings {
		change[b[0]-1] += b[2]
		change[b[1]] -= b[2]
	}
	seats := make([]int64, 0, n)
	var running int64
	for i := int64(0); i < n; i++ {
		running += change[i]
		seats = append(seats, running)
	}
	return seats
}

var seed int64 = 1109

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func booking(n int64) []int64 {
	a := nextRandom()%n + 1
	b := nextRandom()%n + 1
	if a > b {
		a, b = b, a
	}
	return []int64{a, b, nextRandom()%10000 + 1}
}

func main() {
	var n int64 = 20000
	problems := make([][][]int64, 16)
	for j := range problems {
		problems[j] = make([][]int64, 20000)
		for i := range problems[j] {
			problems[j][i] = booking(n)
		}
	}
	var busiest, check int64
	for round := 0; round < 200; round++ {
		for j := range problems {
			at := (round*7919 + j*104729) % 20000
			problems[j][at] = booking(n)
			seats := corpFlightBookings(problems[j], n)
			most := seats[0]
			for _, s := range seats[1:] {
				if s > most {
					most = s
				}
			}
			busiest += most
			check = (check*31 + seats[(int64(round)*31+int64(j))%n]) % 1000000007
		}
	}
	fmt.Printf("200 rounds over 16 problems of 20000 flights: busiest total %d, checksum %d\n", busiest, check)
}
