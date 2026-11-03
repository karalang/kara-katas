// Benchmark lane for LeetCode 1041 -- Go mirror of robot_bounded.kara.
package main

import (
	"fmt"
	"strings"
)

func isRobotBounded(instructions string) bool {
	var x, y int64
	// north, east, south, west
	var facing int64
	for _, c := range instructions {
		if c == 'G' {
			if facing == 0 {
				y++
			} else if facing == 1 {
				x++
			} else if facing == 2 {
				y--
			} else {
				x--
			}
		} else if c == 'L' {
			facing = (facing + 3) % 4
		} else {
			facing = (facing + 1) % 4
		}
	}
	return (x == 0 && y == 0) || facing != 0
}

var seed int64 = 1041

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 2000, 100, 500
	letters := "GLR"
	strs := make([]string, 0, count)
	for k := 0; k < count; k++ {
		var b strings.Builder
		for i := 0; i < size; i++ {
			r := nextRandom() % 10
			var c byte
			if k%2 == 0 {
				c = letters[r%3]
			} else if r < 8 {
				c = 'G'
			} else if r == 8 {
				c = 'L'
			} else {
				c = 'R'
			}
			b.WriteByte(c)
		}
		strs = append(strs, b.String())
	}
	var bounded, check int64
	for r := 0; r < rounds; r++ {
		for _, s := range strs {
			answer := isRobotBounded(s)
			if answer {
				bounded++
			}
			var v int64 = 1
			if answer {
				v = 2
			}
			check = (check*131 + v) % 1000000007
		}
	}
	fmt.Printf("%d strings of %d instructions, %d rounds: %d bounded, checksum %d\n", count, size, rounds, bounded, check)
}
