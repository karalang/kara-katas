// LeetCode #1634: Add Two Polynomials Represented as Linked Lists -- the
// bench's Go mirror: the ★ arm on 10 random pairs of polynomials with
// powers below 400000, all drawn first as terms; each pair is built into
// two lists and added.
package main

import "fmt"

type PolyNode struct {
	coefficient, power int64
	next                *PolyNode
}

func addPoly(poly1, poly2 *PolyNode) *PolyNode {
	head := &PolyNode{}
	tail := head
	a, b := poly1, poly2
	for a != nil || b != nil {
		var coefficient, power int64
		switch {
		case a != nil && b != nil && a.power == b.power:
			coefficient, power = a.coefficient+b.coefficient, a.power
			a, b = a.next, b.next
		case a != nil && b != nil && a.power < b.power:
			coefficient, power = b.coefficient, b.power
			b = b.next
		case a != nil:
			coefficient, power = a.coefficient, a.power
			a = a.next
		default:
			coefficient, power = b.coefficient, b.power
			b = b.next
		}
		if coefficient != 0 {
			node := &PolyNode{coefficient, power, nil}
			tail.next = node
			tail = node
		}
	}
	return head.next
}

var seed int64 = 1634

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func fromTerms(terms [][2]int64) *PolyNode {
	var head *PolyNode
	for i := len(terms) - 1; i >= 0; i-- {
		head = &PolyNode{terms[i][0], terms[i][1], head}
	}
	return head
}

func randomTerms() [][2]int64 {
	var terms [][2]int64
	for power := int64(399999); power >= 0; power-- {
		if nextRandom()%2 == 0 {
			coefficient := nextRandom()%6 - 3
			if coefficient >= 0 {
				coefficient++
			}
			terms = append(terms, [2]int64{coefficient, power})
		}
	}
	return terms
}

func main() {
	pairs := make([][2][][2]int64, 0, 10)
	for i := 0; i < 10; i++ {
		poly1 := randomTerms()
		poly2 := randomTerms()
		pairs = append(pairs, [2][][2]int64{poly1, poly2})
	}
	var check, terms int64
	for _, pair := range pairs {
		for node := addPoly(fromTerms(pair[0]), fromTerms(pair[1])); node != nil; node = node.next {
			terms++
			check = ((check*31+node.coefficient+1000000)%1000000007*31 + node.power) % 1000000007
		}
	}
	fmt.Printf("10 pairs of up to 400000 terms: %d terms, checksum %d\n", terms, check)
}
