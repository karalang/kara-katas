// LeetCode #2029: Stone Game IX -- the ★ arm in Go, the same algorithm and
// workload as stones.kara.
package main

import "fmt"

func stoneGameIX(stones []int64) bool {
	var cnt [3]int64
	for _, s := range stones {
		cnt[s%3]++
	}
	if cnt[0]%2 == 0 {
		return cnt[1] >= 1 && cnt[2] >= 1
	}
	d := cnt[1] - cnt[2]
	if d < 0 {
		d = -d
	}
	return d > 2
}

var seed int64 = 2029

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	games := make([][]int64, 20)
	for a := int64(0); a < 20; a++ {
		stones := make([]int64, 0, 100000)
		for i := 0; i < 100000; i++ {
			base := 3 * (nextRandom() % 3333)
			var residue int64
			if nextRandom()%10 < a%5 {
				residue = 3
			} else if nextRandom()%10 < 3*a%11 {
				residue = 1
			} else {
				residue = 2
			}
			stones = append(stones, base+residue)
		}
		games[a] = stones
	}
	var calls, wins, check int64
	for round := 0; round < 100; round++ {
		for a := 0; a < 20; a++ {
			games[a][(round*997+a*31)%100000]++
			answer := stoneGameIX(games[a])
			calls++
			if answer {
				wins++
			}
			v := int64(2)
			if answer {
				v = 1
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("%d calls: Alice wins %d, checksum %d\n", calls, wins, check)
}
