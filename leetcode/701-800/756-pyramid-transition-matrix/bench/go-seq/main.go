// LeetCode 756 — Pyramid Transition Matrix: benchmark, the ★ arm in Go.
package main

import "fmt"

func rowCode(row []int64) int64 {
	code := int64(1)
	for _, x := range row {
		code = code*6 + x
	}
	return code
}

func fill(row []int64, i int, next *[]int64, table []int64, dead map[int64]struct{}) bool {
	if i+1 == len(row) {
		return build(*next, table, dead)
	}
	options := table[row[i]*6+row[i+1]]
	block := int64(0)
	for options > 0 {
		if options&1 == 1 {
			*next = append(*next, block)
			if fill(row, i+1, next, table, dead) {
				return true
			}
			*next = (*next)[:len(*next)-1]
		}
		options >>= 1
		block++
	}
	return false
}

func build(row []int64, table []int64, dead map[int64]struct{}) bool {
	if len(row) == 1 {
		return true
	}
	code := rowCode(row)
	if _, ok := dead[code]; ok {
		return false
	}
	next := []int64{}
	if fill(row, 0, &next, table, dead) {
		return true
	}
	dead[code] = struct{}{}
	return false
}

func pyramidTransition(bottom string, allowed []string) bool {
	table := make([]int64, 36)
	for _, t := range allowed {
		pair := int(t[0]-'A')*6 + int(t[1]-'A')
		table[pair] |= 1 << (t[2] - 'A')
	}
	row := []int64{}
	for i := 0; i < len(bottom); i++ {
		row = append(row, int64(bottom[i]-'A'))
	}
	dead := map[int64]struct{}{}
	return build(row, table, dead)
}

var seed int64 = 756

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := int64(200000)
	yes := int64(0)
	check := int64(0)
	for round := int64(0); round < rounds; round++ {
		bottom := []byte{}
		for i := 0; i < 6; i++ {
			bottom = append(bottom, byte('A'+nextRandom()%6))
		}
		count := 40 + nextRandom()%80
		allowed := []string{}
		for t := int64(0); t < count; t++ {
			b := []byte{}
			for j := 0; j < 3; j++ {
				b = append(b, byte('A'+nextRandom()%6))
			}
			allowed = append(allowed, string(b))
		}
		if pyramidTransition(string(bottom), allowed) {
			yes++
			check = (check*31 + round) % 1000000007
		}
	}
	fmt.Printf("%d pyramids of width 6: %d can be built, checksum %d\n", rounds, yes, check)
}
