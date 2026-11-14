// LeetCode #1560: Most Visited Sector in a Circular Track -- bench: the ★
// arm (the sectors from the first on to the last, wrapping past n) over
// 20000 tracks of up to 100 sectors and 100 legs, built once, each asked
// 100 times.
// Go mirror of sectors.kara.
package main

import "fmt"

func mostVisited(n int64, rounds []int64) []int64 {
	start := rounds[0]
	end := rounds[len(rounds)-1]
	var out []int64
	if start <= end {
		for s := start; s <= end; s++ {
			out = append(out, s)
		}
	} else {
		for s := int64(1); s <= end; s++ {
			out = append(out, s)
		}
		for s := start; s <= n; s++ {
			out = append(out, s)
		}
	}
	return out
}

var seed int64 = 1560

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type track struct {
	n      int64
	rounds []int64
}

func main() {
	tracks := make([]track, 0, 20000)
	for i := 0; i < 20000; i++ {
		n := nextRandom()%99 + 2
		m := nextRandom()%100 + 1
		rounds := []int64{nextRandom()%n + 1}
		for j := int64(0); j < m; j++ {
			at := rounds[len(rounds)-1]
			rounds = append(rounds, (at-1+nextRandom()%(n-1)+1)%n+1)
		}
		tracks = append(tracks, track{n, rounds})
	}
	var check, total int64
	for pass := int64(0); pass < 100; pass++ {
		for t, tr := range tracks {
			sectors := mostVisited(tr.n, tr.rounds)
			total += int64(len(sectors))
			check = mix(check, sectors[(pass*7+int64(t))%int64(len(sectors))])
		}
	}
	fmt.Printf("100 passes over 20000 tracks: %d sectors, checksum %d\n", total, check)
}
