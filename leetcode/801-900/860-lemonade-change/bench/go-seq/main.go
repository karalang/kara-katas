// LeetCode #860: Lemonade Change -- Go mirror of the bench program (the ★
// arm, count the fives and tens, pay a twenty with a ten when there is one).
package main

import "fmt"

func lemonadeChange(bills []int64) bool {
	var fives, tens int64
	for _, b := range bills {
		if b == 5 {
			fives++
		} else if b == 10 {
			if fives == 0 {
				return false
			}
			fives--
			tens++
		} else if tens > 0 && fives > 0 {
			tens--
			fives--
		} else if fives >= 3 {
			fives -= 3
		} else {
			return false
		}
	}
	return true
}

var seed int64 = 860

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var n int64 = 100000
	bills := make([]int64, 0, n)
	var fives, tens int64
	for k := int64(0); k < n; k++ {
		r := nextRandom() % 10
		if r >= 8 && tens > 0 && fives > 0 {
			bills = append(bills, 20)
			tens--
			fives--
		} else if r >= 8 && fives >= 3 {
			bills = append(bills, 20)
			fives -= 3
		} else if r >= 5 && fives > 0 {
			bills = append(bills, 10)
			fives--
			tens++
		} else {
			bills = append(bills, 5)
			fives++
		}
	}
	var served, check int64
	for r := int64(0); r < 1000; r++ {
		i := nextRandom() % n
		old := bills[i]
		if old == 5 {
			bills[i] = 10
		} else if old == 10 {
			bills[i] = 20
		} else {
			bills[i] = 5
		}
		yes := lemonadeChange(bills)
		bills[i] = old
		if yes {
			served++
		}
		add := int64(1)
		if yes {
			add = r + 2
		}
		check = (check*31 + add) % 1000000007
	}
	fmt.Printf("1000 rounds on 100000 bills: %d served, checksum %d\n", served, check)
}
