// LeetCode #2015: Average Height of Buildings in Each Segment -- the ★ arm's
// benchmark, a mirror of average.kara.
package main

import (
	"fmt"
	"sort"
)

type triple struct{ a, b, c int64 }

func averageHeightOfBuildings(buildings []triple) []triple {
	events := make([]triple, 0, 2*len(buildings))
	for _, b := range buildings {
		events = append(events, triple{b.a, b.c, 1}, triple{b.b, -b.c, -1})
	}
	sort.Slice(events, func(i, j int) bool {
		p, q := events[i], events[j]
		if p.a != q.a {
			return p.a < q.a
		}
		if p.b != q.b {
			return p.b < q.b
		}
		return p.c < q.c
	})
	var street []triple
	var sum, count int64
	i := 0
	for i < len(events) {
		at := events[i].a
		for i < len(events) && events[i].a == at {
			sum += events[i].b
			count += events[i].c
			i++
		}
		if count == 0 {
			continue
		}
		next := events[i].a
		average := sum / count
		n := len(street)
		if n > 0 && street[n-1].b == at && street[n-1].c == average {
			street[n-1].b = next
		} else {
			street = append(street, triple{at, next, average})
		}
	}
	return street
}

var seed int64 = 2015

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	streets := make([][]triple, 0, 60)
	for s := int64(0); s < 60; s++ {
		buildings := make([]triple, 0, 10000)
		for k := 0; k < 10000; k++ {
			a := nextRandom()
			start := (a*32768 + nextRandom()) % 1000000
			end := start + nextRandom()%(100*(s+1)) + 1
			buildings = append(buildings, triple{start, end, nextRandom()%(s+2) + 1})
		}
		streets = append(streets, buildings)
	}
	var calls, segments, check int64
	for r := 0; r < 5; r++ {
		for _, buildings := range streets {
			street := averageHeightOfBuildings(buildings)
			calls++
			segments += int64(len(street))
			for _, t := range street {
				check = (check*31 + t.a + t.b*7 + t.c*13) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d segments, checksum %d\n", calls, segments, check)
}
