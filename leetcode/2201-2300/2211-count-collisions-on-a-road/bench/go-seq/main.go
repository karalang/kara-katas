// benchmark's Go mirror of collisions.kara (LeetCode #2211, the ★ arm):
// skip the leading 'L's and the trailing 'R's and count the cars between
// that are not 'S'. The road is collected rune by rune, as Kāra's
// `chars()`.
package main

import (
	"fmt"
	"strings"
)

func countCollisions(directions string) int64 {
	cars := []rune(directions)
	lo := 0
	for lo < len(cars) && cars[lo] == 'L' {
		lo++
	}
	hi := len(cars)
	for hi > lo && cars[hi-1] == 'R' {
		hi--
	}
	var count int64
	for _, car := range cars[lo:hi] {
		if car != 'S' {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2211)
	letters := []byte{'L', 'R', 'S'}
	roads := []string{}
	for r := 0; r < 20; r++ {
		// a run of left-movers at the front and right-movers at the back,
		// each r thousand cars long, around random cars
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			if i < r*1000 {
				b.WriteByte('L')
			} else if i >= 100000-r*1000 {
				b.WriteByte('R')
			} else {
				b.WriteByte(letters[nextRandom(&seed)%3])
			}
		}
		roads = append(roads, b.String())
	}
	check := int64(0)
	for p := int64(0); p < 10; p++ {
		for _, road := range roads {
			check = (check*31 + countCollisions(road) + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 20 roads: checksum %d\n", check)
}
