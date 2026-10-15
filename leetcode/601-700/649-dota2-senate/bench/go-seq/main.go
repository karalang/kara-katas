// LeetCode #649: Dota2 Senate -- Go mirror of the Kāra bench.
//
// The ★ arm over the same senates and rounds: a slice used as a queue
// for each party's senators by when they vote, the front two meeting and
// the earlier going to the back `n` places later.
package main

import (
	"fmt"
	"strings"
)

func predictPartyVictory(senate string) string {
	n := int64(len(senate))
	var radiant, dire []int64
	for i := int64(0); i < n; i++ {
		if senate[i] == 'R' {
			radiant = append(radiant, i)
		} else {
			dire = append(dire, i)
		}
	}
	for len(radiant) > 0 && len(dire) > 0 {
		r, d := radiant[0], dire[0]
		radiant, dire = radiant[1:], dire[1:]
		if r < d {
			radiant = append(radiant, r+n)
		} else {
			dire = append(dire, d+n)
		}
	}
	if len(radiant) > 0 {
		return "Radiant"
	}
	return "Dire"
}

var seed int64 = 649

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const inputs = 20
	const rounds = 500
	senates := make([]string, 0, inputs)
	for i := 0; i < inputs; i++ {
		radiant := 45 + nextRandom()%11
		var b strings.Builder
		for j := 0; j < 100000; j++ {
			if nextRandom()%100 < radiant {
				b.WriteByte('R')
			} else {
				b.WriteByte('D')
			}
		}
		senates = append(senates, b.String())
	}
	var wins, checksum int64
	for r := 0; r < rounds; r++ {
		won := predictPartyVictory(senates[(r*7)%inputs]) == "Radiant"
		var bit int64
		if won {
			wins++
			bit = 1
		}
		checksum = (checksum*2 + bit) % 1000000007
	}
	fmt.Printf("%d senates, %d rounds: Radiant wins %d, checksum %d\n", inputs, rounds, wins, checksum)
}
