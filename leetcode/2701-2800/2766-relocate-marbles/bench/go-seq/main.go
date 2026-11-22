// LeetCode #2766: Relocate Marbles -- the bench (marbles.kara in Go): the
// occupied positions in a map used as a set, each move taking its from
// position out and putting its to position in, sorted at the end.
package main

import (
	"fmt"
	"slices"
)

var seed int64 = 2766

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func relocateMarbles(nums, moveFrom, moveTo []int64) []int64 {
	occupied := make(map[int64]struct{}, len(nums))
	for _, x := range nums {
		occupied[x] = struct{}{}
	}
	for i := range moveFrom {
		delete(occupied, moveFrom[i])
		occupied[moveTo[i]] = struct{}{}
	}
	places := make([]int64, 0, len(occupied))
	for p := range occupied {
		places = append(places, p)
	}
	slices.Sort(places)
	return places
}

func makeCase(n, moves, top int64) ([]int64, []int64, []int64) {
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = wide()%top + 1
	}
	places := make([]int64, 0, n)
	slot := make([]int64, top+1)
	for i := range slot {
		slot[i] = -1
	}
	for _, x := range nums {
		if slot[x] < 0 {
			slot[x] = int64(len(places))
			places = append(places, x)
		}
	}
	moveFrom := make([]int64, moves)
	moveTo := make([]int64, moves)
	for i := range moveFrom {
		a := places[wide()%int64(len(places))]
		b := wide()%top + 1
		moveFrom[i], moveTo[i] = a, b
		if a != b {
			k := slot[a]
			slot[a] = -1
			last := places[len(places)-1]
			places = places[:len(places)-1]
			if last != a {
				places[k] = last
				slot[last] = k
			}
			if slot[b] < 0 {
				slot[b] = int64(len(places))
				places = append(places, b)
			}
		}
	}
	return nums, moveFrom, moveTo
}

func main() {
	const count, rounds = 20, 5
	type caseT struct{ nums, from, to []int64 }
	cases := make([]caseT, count)
	for c := range cases {
		a, b, d := makeCase(100000, 100000, 1000000)
		cases[c] = caseT{a, b, d}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, cs := range cases {
			places := relocateMarbles(cs.nums, cs.from, cs.to)
			k := int64(len(places))
			sum += k
			check = (check*31 + k + r) % 1000000007
			for _, p := range places {
				check = (check*31 + p) % 1000000007
			}
		}
	}
	fmt.Printf("%d cases of 100000 marbles and moves, %d rounds: %d places, checksum %d\n", count, rounds, sum, check)
}
