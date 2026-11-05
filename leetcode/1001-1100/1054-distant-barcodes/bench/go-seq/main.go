// LeetCode #1054: Distant Barcodes -- Go mirror of bench/barcodes.kara.
package main

import "fmt"

var seed int64 = 1054

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func rearrangeBarcodes(barcodes []int64) []int64 {
	n := len(barcodes)
	top := barcodes[0]
	for _, b := range barcodes {
		if b > top {
			top = b
		}
	}
	counts := make([]int64, top+1)
	for _, b := range barcodes {
		counts[b]++
	}
	var most int64
	for v := int64(1); v < top+1; v++ {
		if counts[v] > counts[most] {
			most = v
		}
	}
	answer := make([]int64, n)
	place := 0
	v := most
	var next int64 = 1
	for k := 0; k < n; k++ {
		for counts[v] == 0 {
			v = next
			next++
		}
		answer[place] = v
		counts[v]--
		place += 2
		if place >= n {
			place = 1
		}
	}
	return answer
}

func main() {
	const count, n, rounds = 200, 20000, 25
	all := make([][]int64, 0, count)
	for a := 0; a < count; a++ {
		common := nextRandom()%10000 + 1
		copies := nextRandom()%9000 + 1
		barcodes := make([]int64, 0, n)
		for k := int64(0); k < copies; k++ {
			barcodes = append(barcodes, common)
		}
		for k := copies; k < n; k++ {
			barcodes = append(barcodes, nextRandom()%10000+1)
		}
		all = append(all, barcodes)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, barcodes := range all {
			answer := rearrangeBarcodes(barcodes)
			var h int64
			for k := 0; k < n; k += 97 {
				h = (h*10007 + answer[k]) % 1000000007
			}
			total += answer[1]
			check = (check*131 + h) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d barcodes, %d rounds: total %d, checksum %d\n", count, n, rounds, total, check)
}
