// LeetCode #2147: Number of Ways to Divide a Long Corridor -- the
// benchmark's Go mirror of corridor.kara.
package main

import (
	"fmt"
	"strings"
)

const mod = 1000000007

func numberOfWays(corridor string) int64 {
	seats := []int64{}
	for i, ch := range corridor {
		if ch == 'S' {
			seats = append(seats, int64(i))
		}
	}
	if len(seats) == 0 || len(seats)%2 == 1 {
		return 0
	}
	var ways int64 = 1
	for p := 2; p < len(seats); p += 2 {
		ways = ways * (seats[p] - seats[p-1]) % mod
	}
	return ways
}

var seed int64 = 2147

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	corridors := []string{}
	for c := 0; c < 4; c++ {
		var b strings.Builder
		count := 0
		for i := 0; i < 99999; i++ {
			if nextRandom()%3 == 0 {
				b.WriteByte('S')
				count++
			} else {
				b.WriteByte('P')
			}
		}
		if count%2 == 1 {
			b.WriteByte('S')
		} else {
			b.WriteByte('P')
		}
		corridors = append(corridors, b.String())
	}
	var total, check int64
	for round := int64(0); round < 25; round++ {
		for c := 0; c < 4; c++ {
			i := nextRandom() % 99999
			place := corridors[c]
			corridors[c] = place[:i] + place[i+1:i+2] + place[i:i+1] + place[i+2:]
			ways := numberOfWays(corridors[c])
			total = (total + ways) % mod
			check = (check*31 + ways + round) % mod
		}
	}
	fmt.Printf("100 counts: %d ways in all, checksum %d\n", total, check)
}
