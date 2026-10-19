// LeetCode 772 — Basic Calculator III: benchmark, the ★ arm in Go.
// Sixty-four random expressions of 2,400 numbers, up to LeetCode's limit
// of 10,000 characters, built once; ROUNDS rounds each evaluate the next.
// At each operator the generator takes the first, from a random start,
// that keeps every value valid: no division by zero, nothing beyond 32
// bits.
package main

import (
	"fmt"
	"strconv"
)

const ROUNDS = 6000
const LEAVES = 2400

type Cursor struct {
	s  string
	at int
}

func (c *Cursor) peek() byte {
	if c.at < len(c.s) {
		return c.s[c.at]
	}
	return 0
}

func (c *Cursor) sum() int64 {
	value := c.term()
	for {
		op := c.peek()
		if op != '+' && op != '-' {
			return value
		}
		c.at++
		right := c.term()
		if op == '+' {
			value += right
		} else {
			value -= right
		}
	}
}

func (c *Cursor) term() int64 {
	value := c.factor()
	for {
		op := c.peek()
		if op != '*' && op != '/' {
			return value
		}
		c.at++
		right := c.factor()
		if op == '*' {
			value *= right
		} else {
			value /= right
		}
	}
}

func (c *Cursor) factor() int64 {
	if c.peek() == '(' {
		c.at++
		value := c.sum()
		c.at++
		return value
	}
	var value int64
	for c.peek() >= '0' && c.peek() <= '9' {
		value = value*10 + int64(c.peek()-'0')
		c.at++
	}
	return value
}

func calculate(s string) int64 {
	c := Cursor{s, 0}
	return c.sum()
}

var seed int64 = 772

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func combine(a int64, op byte, b int64) (int64, bool) {
	if op == '/' && b == 0 {
		return 0, false
	}
	var v int64
	switch op {
	case '+':
		v = a + b
	case '-':
		v = a - b
	case '*':
		v = a * b
	default:
		v = a / b
	}
	if v < -2147483648 || v > 2147483647 {
		return 0, false
	}
	return v, true
}

type Piece struct {
	text  string
	value int64
	level int
}

func build(leaves int64) Piece {
	if leaves == 1 {
		var n int64
		if nextRandom()%4 == 0 {
			n = nextRandom() % 1000
		} else {
			n = nextRandom() % 10
		}
		return Piece{strconv.FormatInt(n, 10), n, 3}
	}
	leftLeaves := 1 + nextRandom()%(leaves-1)
	left := build(leftLeaves)
	right := build(leaves - leftLeaves)
	ops := "+-*/"
	k := nextRandom() % 4
	for {
		if _, ok := combine(left.value, ops[k], right.value); ok {
			break
		}
		k = (k + 1) % 4
	}
	op := ops[k]
	value, _ := combine(left.value, op, right.value)
	level := 2
	if op == '+' || op == '-' {
		level = 1
	}
	leftText := left.text
	if left.level < level || nextRandom()%4 == 0 {
		leftText = "(" + left.text + ")"
	}
	rightText := right.text
	if right.level < level || (right.level == level && op != '+') || nextRandom()%4 == 0 {
		rightText = "(" + right.text + ")"
	}
	return Piece{leftText + string(op) + rightText, value, level}
}

func main() {
	pool := make([]string, 0, 64)
	longest := 0
	for i := 0; i < 64; i++ {
		piece := build(LEAVES)
		if len(piece.text) > longest {
			longest = len(piece.text)
		}
		pool = append(pool, piece.text)
	}
	var check int64
	for round := 0; round < ROUNDS; round++ {
		value := calculate(pool[round%64])
		check = ((check*31+value)%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("%d expressions of up to %d characters: checksum %d\n", ROUNDS, longest, check)
}
