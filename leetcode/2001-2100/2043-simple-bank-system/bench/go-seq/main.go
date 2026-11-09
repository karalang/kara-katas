// LeetCode #2043: Simple Bank System -- the ★ arm in Go, the same algorithm
// and workload as bank.kara: the balances in a slice indexed by account -
// 1, every call checked whole before anything changes.
package main

import "fmt"

type Bank struct {
	balance []int64
}

func (b *Bank) exists(account int64) bool {
	return account >= 1 && account <= int64(len(b.balance))
}

func (b *Bank) Transfer(account1, account2, money int64) bool {
	if !b.exists(account1) || !b.exists(account2) || b.balance[account1-1] < money {
		return false
	}
	b.balance[account1-1] -= money
	b.balance[account2-1] += money
	return true
}

func (b *Bank) Deposit(account, money int64) bool {
	if !b.exists(account) {
		return false
	}
	b.balance[account-1] += money
	return true
}

func (b *Bank) Withdraw(account, money int64) bool {
	if !b.exists(account) || b.balance[account-1] < money {
		return false
	}
	b.balance[account-1] -= money
	return true
}

var seed int64 = 2043

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	hi := nextRandom()
	mid := nextRandom()
	return (hi*32768+mid)*32768 + nextRandom()
}

type op struct{ kind, a, b, money int64 }

func main() {
	const n, callsPer, top = 100000, 1000000, 1000000
	balance := make([]int64, n)
	for i := range balance {
		balance[i] = bigRandom() % (top + 1)
	}
	ops := make([]op, callsPer)
	for i := range ops {
		kind := nextRandom() % 3
		a := bigRandom() % (n + 2)
		b := bigRandom() % (n + 2)
		ops[i] = op{kind, a, b, bigRandom() % (top + 1)}
	}
	var calls, succeeded, check int64
	for round := int64(0); round < 40; round++ {
		bank := Bank{append([]int64(nil), balance...)}
		for _, o := range ops {
			var ok bool
			switch o.kind {
			case 0:
				ok = bank.Transfer(o.a, o.b, o.money)
			case 1:
				ok = bank.Deposit(o.a, o.money)
			default:
				ok = bank.Withdraw(o.a, o.money)
			}
			calls++
			if ok {
				succeeded++
				check = (check*31 + calls + round) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d succeed, checksum %d\n", calls, succeeded, check)
}
