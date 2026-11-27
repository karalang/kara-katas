// LeetCode #1812: Determine Color of a Chessboard Square -- the bench in
// Go: the ★ arm over 3 * 10^7 calls, each of the 64 square names built once
// and drawn from the checksum so far.
package main

import "fmt"

func squareIsWhite(coordinates string) bool {
	file := int64(coordinates[0] - 'a')
	rank := int64(coordinates[1] - '1')
	return (file+rank)%2 == 1
}

func main() {
	names := []string{}
	for _, file := range "abcdefgh" {
		for rank := 1; rank < 9; rank++ {
			names = append(names, fmt.Sprintf("%c%d", file, rank))
		}
	}
	var check int64
	for call := int64(0); call < 30000000; call++ {
		name := names[(check+call)%64]
		var v int64 = 2
		if squareIsWhite(name) {
			v = 1
		}
		check = (check*3 + v) % 1000000007
	}
	fmt.Printf("30000000 calls: checksum %d\n", check)
}
