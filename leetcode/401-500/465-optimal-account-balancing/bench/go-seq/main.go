// Benchmark for #465: mirror of min_transfers.kara (the ★ arm:
// backtracking over the unsettled balances) on the same workload.
package main

import "fmt"

func fewestFrom(debts []int64, start int) int64 {
	first := start
	for first < len(debts) && debts[first] == 0 {
		first++
	}
	if first == len(debts) {
		return 0
	}
	best := int64(-1)
	for j := first + 1; j < len(debts); j++ {
		if debts[j]*debts[first] < 0 {
			debts[j] += debts[first]
			count := 1 + fewestFrom(debts, first+1)
			debts[j] -= debts[first]
			if best < 0 || count < best {
				best = count
			}
		}
	}
	return best
}

func minTransfers(transactions [][3]int64) int64 {
	people := int64(0)
	for _, t := range transactions {
		people = max(people, t[0]+1, t[1]+1)
	}
	balance := make([]int64, people)
	for _, t := range transactions {
		balance[t[0]] -= t[2]
		balance[t[1]] += t[2]
	}
	debts := []int64{}
	for _, b := range balance {
		if b != 0 {
			debts = append(debts, b)
		}
	}
	return fewestFrom(debts, 0)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const ledgers = 20000
	seed := int64(465)
	total := int64(0)
	checksum := int64(0)
	for l := 0; l < ledgers; l++ {
		transactions := [][3]int64{}
		for t := 0; t < 8; t++ {
			from := nextRandom(&seed) % 12
			to := (from + 1 + nextRandom(&seed)%11) % 12
			amount := 1 + nextRandom(&seed)%3
			transactions = append(transactions, [3]int64{from, to, amount})
		}
		fewest := minTransfers(transactions)
		total += fewest
		checksum = (checksum*31 + fewest) % 1000000007
	}
	fmt.Printf("%d ledgers of 8 transactions: %d transfers in all, checksum %d\n", ledgers, total, checksum)
}
