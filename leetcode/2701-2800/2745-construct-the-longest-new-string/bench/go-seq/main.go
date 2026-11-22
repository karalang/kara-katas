// LeetCode #2745: Construct the Longest New String -- the bench
// (longest.kara in Go): the table arm, bottom up over the pieces left and
// the last piece placed, flat in one slice.
package main

import "fmt"

func longestString(x, y, z int64) int64 {
	at := func(a, b, c, last int64) int64 { return ((a*(y+1)+b)*(z+1)+c)*4 + last }
	more := make([]int64, (x+1)*(y+1)*(z+1)*4)
	for a := int64(0); a <= x; a++ {
		for b := int64(0); b <= y; b++ {
			for c := int64(0); c <= z; c++ {
				for last := int64(0); last < 4; last++ {
					var best int64
					if a > 0 && last != 0 {
						best = max(best, 2+more[at(a-1, b, c, 0)])
					}
					if b > 0 && (last == 0 || last == 3) {
						best = max(best, 2+more[at(a, b-1, c, 1)])
					}
					if c > 0 && last != 0 {
						best = max(best, 2+more[at(a, b, c-1, 2)])
					}
					more[at(a, b, c, last)] = best
				}
			}
		}
	}
	return more[at(x, y, z, 3)]
}

var seed int64 = 2745

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 1000, 3
	cases := [][3]int64{}
	for k := 0; k < count; k++ {
		x := nextRandom()%50 + 1
		y := nextRandom()%50 + 1
		z := nextRandom()%50 + 1
		cases = append(cases, [3]int64{x, y, z})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, c := range cases {
			length := longestString(c[0], c[1], c[2])
			sum += length
			check = (check*31 + length + r) % 1000000007
		}
	}
	fmt.Printf("%d counts, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, sum, check)
}
