// LeetCode #1169: Invalid Transactions -- the ★ arm's bench in Go: each
// transaction split into its fields, the places of each name's
// transactions gathered in a map, and every transaction compared with the
// others of its name.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type txn struct {
	name         string
	time, amount int64
	city         string
}

func parse(t string) txn {
	f := strings.Split(t, ",")
	time, _ := strconv.ParseInt(f[1], 10, 64)
	amount, _ := strconv.ParseInt(f[2], 10, 64)
	return txn{f[0], time, amount, f[3]}
}

func invalidTransactions(transactions []string) []string {
	txns := make([]txn, len(transactions))
	byName := map[string][]int{}
	for i, t := range transactions {
		txns[i] = parse(t)
		byName[txns[i].name] = append(byName[txns[i].name], i)
	}
	var out []string
	for i, t := range txns {
		bad := t.amount > 1000
		if !bad {
			for _, j := range byName[t.name] {
				o := txns[j]
				d := o.time - t.time
				if d < 0 {
					d = -d
				}
				if d <= 60 && o.city != t.city {
					bad = true
					break
				}
			}
		}
		if bad {
			out = append(out, transactions[i])
		}
	}
	return out
}

var seed int64 = 1169

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func line() string {
	name := nextRandom() % 200
	time := nextRandom() % 1001
	amount := nextRandom() % 1101
	city := nextRandom() % 2
	return fmt.Sprintf("n%d,%d,%d,c%d", name, time, amount, city)
}

func main() {
	lists := make([][]string, 16)
	for k := range lists {
		for i := 0; i < 1000; i++ {
			lists[k] = append(lists[k], line())
		}
	}
	var total, check int64
	for r := 0; r < 300; r++ {
		for k := 0; k < 16; k++ {
			at := nextRandom() % 1000
			lists[k][at] = line()
			bad := invalidTransactions(lists[k])
			total += int64(len(bad))
			for _, b := range bad {
				check = (check*31 + int64(len(b))) % 1000000007
			}
		}
	}
	fmt.Printf("300 rounds over 16 lists of 1000 transactions: %d invalid, checksum %d\n", total, check)
}
