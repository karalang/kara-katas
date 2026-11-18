// LeetCode #1612: Check If Two Expression Trees are Equivalent -- the bench
// in Go, mirroring equivalent.kara: one walk counts the first tree's
// leaves up and the second's down, into one array of 26 counts.
package main

import "fmt"

type Node struct {
	Val         byte
	Left, Right *Node
}

func tally(node *Node, sign int32, counts *[26]int32) {
	if node == nil {
		return
	}
	if node.Val == '+' {
		tally(node.Left, sign, counts)
		tally(node.Right, sign, counts)
	} else {
		counts[node.Val-'a'] += sign
	}
}

func checkEquivalence(root1, root2 *Node) bool {
	var counts [26]int32
	tally(root1, 1, &counts)
	tally(root2, -1, &counts)
	for _, c := range counts {
		if c != 0 {
			return false
		}
	}
	return true
}

var seed int64 = 1612

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func randomExpression(leaves []byte) *Node {
	loose := make([]*Node, len(leaves))
	for i, c := range leaves {
		loose[i] = &Node{Val: c}
	}
	for len(loose) > 1 {
		i := big() % int64(len(loose))
		a := loose[i]
		loose[i] = loose[len(loose)-1]
		loose = loose[:len(loose)-1]
		j := big() % int64(len(loose))
		b := loose[j]
		loose[j] = loose[len(loose)-1]
		loose = loose[:len(loose)-1]
		loose = append(loose, &Node{Val: '+', Left: a, Right: b})
	}
	return loose[0]
}

func main() {
	const n = 50000
	var ones, twos [10]*Node
	for p := 0; p < 10; p++ {
		leaves := make([]byte, n)
		for i := range leaves {
			leaves[i] = byte('a' + nextRandom()%26)
		}
		other := append([]byte(nil), leaves...)
		for i := int64(n - 1); i >= 1; i-- {
			j := big() % (i + 1)
			other[i], other[j] = other[j], other[i]
		}
		if nextRandom()%2 == 0 {
			i := big() % n
			other[i] = byte('a' + nextRandom()%26)
		}
		ones[p] = randomExpression(leaves)
		twos[p] = randomExpression(other)
	}
	var check, equivalent int64
	for p := 0; p < 10; p++ {
		for k := 0; k < 10; k++ {
			var same bool
			if k%2 == 0 {
				same = checkEquivalence(ones[p], twos[p])
			} else {
				same = checkEquivalence(twos[p], ones[p])
			}
			var x int64
			if same {
				equivalent++
				x = 1
			}
			check = (check*31 + x + 1) % 1000000007
		}
	}
	fmt.Printf("10 pairs of 50000 leaves from 26 letters, 100 checks: %d equivalent, checksum %d\n", equivalent, check)
}
