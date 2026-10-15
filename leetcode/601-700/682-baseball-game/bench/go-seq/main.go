// LeetCode #682: Baseball Game -- a stack of the valid scores. Bench.
package main

import (
	"fmt"
	"strconv"
)

var seed int64 = 682

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func calPoints(operations []string) int64 {
	var record []int64
	for _, op := range operations {
		switch op {
		case "+":
			n := len(record)
			record = append(record, record[n-1]+record[n-2])
		case "D":
			record = append(record, record[len(record)-1]*2)
		case "C":
			record = record[:len(record)-1]
		default:
			x, _ := strconv.ParseInt(op, 10, 64)
			record = append(record, x)
		}
	}
	var total int64
	for _, x := range record {
		total += x
	}
	return total
}

func randomOps(n int) []string {
	const limit = 1073741824
	var record []int64
	var out []string
	for len(out) < n {
		k := len(record)
		pick := nextRandom() % 10
		if pick == 0 && k >= 1 {
			record = record[:k-1]
			out = append(out, "C")
		} else if pick == 1 && k >= 1 && abs(record[k-1]) < limit/2 {
			record = append(record, record[k-1]*2)
			out = append(out, "D")
		} else if pick == 2 && k >= 2 && abs(record[k-1]+record[k-2]) < limit {
			record = append(record, record[k-1]+record[k-2])
			out = append(out, "+")
		} else if pick >= 3 {
			x := nextRandom()%60001 - 30000
			record = append(record, x)
			out = append(out, strconv.FormatInt(x, 10))
		}
	}
	return out
}

func main() {
	const count, rounds = 200, 30
	lists := make([][]string, count)
	for k := range lists {
		lists[k] = randomOps(5000)
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for k := int64(0); k < count; k++ {
			at := (k*7 + r) % count
			points := calPoints(lists[at])
			sum = (sum*31 + points%1000000007 + 1000000007) % 1000000007
		}
	}
	fmt.Printf("%d games scored, checksum %d\n", count*rounds, sum)
}
