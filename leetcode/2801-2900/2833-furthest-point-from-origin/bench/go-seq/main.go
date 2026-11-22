// LeetCode #2833: Furthest Point From Origin -- the bench, mirrored from
// furthest.kara: the L and R counts, and the blanks.
package main

import "fmt"

func furthestDistanceFromOrigin(moves string) int64 {
	var left, right int64
	for _, c := range moves {
		if c == 'L' {
			left++
		}
	}
	for _, c := range moves {
		if c == 'R' {
			right++
		}
	}
	gap := left - right
	if gap < 0 {
		gap = -gap
	}
	return gap + int64(len(moves)) - left - right
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 100000, 100, 50
	seed := int64(2833)
	strings := make([]string, 0, count)
	for c := 0; c < count; c++ {
		blank := nextRandom(&seed) % 6
		codes := make([]byte, n)
		for i := range codes {
			r := nextRandom(&seed) % 6
			if r < blank {
				codes[i] = '_'
			} else if r%2 == 0 {
				codes[i] = 'L'
			} else {
				codes[i] = 'R'
			}
		}
		strings = append(strings, string(codes))
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, moves := range strings {
			d := furthestDistanceFromOrigin(moves)
			total += d
			check = (check*31 + d + r) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d, %d rounds: distances total %d, checksum %d\n", count, n, rounds, total, check)
}
