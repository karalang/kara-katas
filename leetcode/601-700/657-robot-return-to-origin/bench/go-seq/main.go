// Benchmark for #657: walk the moves, as the Kara ★ arm.
package main

import (
	"fmt"
	"strings"
)

func judgeCircle(moves string) bool {
	var x, y int64
	for _, m := range moves {
		switch m {
		case 'U':
			y++
		case 'D':
			y--
		case 'L':
			x--
		default:
			x++
		}
	}
	return x == 0 && y == 0
}

var seed int64 = 657

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomMoves(n int64, balanced bool) string {
	letters := []rune{'U', 'D', 'L', 'R'}
	steps := make([]rune, 0, n)
	if balanced {
		for k := int64(0); k < n/2; k++ {
			pair := nextRandom() % 2
			steps = append(steps, letters[pair*2], letters[pair*2+1])
		}
		for i := int64(len(steps)) - 1; i > 0; i-- {
			j := nextRandom() % (i + 1)
			steps[i], steps[j] = steps[j], steps[i]
		}
	} else {
		for k := int64(0); k < n; k++ {
			steps = append(steps, letters[nextRandom()%4])
		}
	}
	var b strings.Builder
	for _, c := range steps {
		b.WriteRune(c)
	}
	return b.String()
}

func main() {
	inputs, rounds := int64(8), int64(100)
	strs := make([]string, inputs)
	for k := int64(0); k < inputs; k++ {
		strs[k] = randomMoves(1000000, k%2 == 0)
	}
	var back, checksum int64
	for r := int64(0); r < rounds; r++ {
		pick := (r * 3) % inputs
		at := judgeCircle(strs[pick])
		bit := int64(0)
		if at {
			back++
			bit = 1
		}
		checksum = (checksum*31 + pick*2 + bit) % 1000000007
	}
	fmt.Printf("%d strings of 1000000, %d rounds: %d back, checksum %d\n", inputs, rounds, back, checksum)
}
