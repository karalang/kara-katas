// LeetCode #2327: Number of People Aware of a Secret -- the bench, the ★
// arm in Go. A running count of the people sharing gains those who
// learned the secret `delay` days back and loses those who learned it
// `forget` days back, and that many learn it each day. O(n).
package main

import "fmt"

const mod = 1000000007

func peopleAwareOfSecret(n, delay, forget int64) int64 {
	learned := make([]int64, n+1)
	learned[1] = 1
	var sharing int64
	for day := int64(2); day <= n; day++ {
		if day-delay >= 1 {
			sharing = (sharing + learned[day-delay]) % mod
		}
		if day-forget >= 1 {
			sharing = (sharing - learned[day-forget] + mod) % mod
		}
		learned[day] = sharing
	}
	var aware int64
	for day := n - forget + 1; day <= n; day++ {
		aware = (aware + learned[day]) % mod
	}
	return aware
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2327)
	delays := make([]int64, 3000)
	forgets := make([]int64, 3000)
	for k := 0; k < 3000; k++ {
		forgets[k] = nextRandom(&seed)%989 + 2
		delays[k] = nextRandom(&seed)%(forgets[k]-1) + 1
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for k := int64(0); k < 3000; k++ {
			n := 990 + (k+p)%11
			check = (check*31 + peopleAwareOfSecret(n, delays[k], forgets[k])) % 1000000007
		}
	}
	fmt.Printf("10 passes over 3000 cases of up to 1000 days: checksum %d\n", check)
}
