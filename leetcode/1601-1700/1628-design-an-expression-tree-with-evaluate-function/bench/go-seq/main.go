// LeetCode #1628: Design an Expression Tree With Evaluate Function -- the
// bench's Go mirror: a Node interface, one struct per operator, on 20000
// random postfix expressions of 50 operands, all drawn first.
package main

import (
	"fmt"
	"strconv"
)

type Node interface {
	Evaluate() int64
}

type Number struct{ value int64 }
type Add struct{ left, right Node }
type Subtract struct{ left, right Node }
type Multiply struct{ left, right Node }
type Divide struct{ left, right Node }

func (n Number) Evaluate() int64   { return n.value }
func (n Add) Evaluate() int64      { return n.left.Evaluate() + n.right.Evaluate() }
func (n Subtract) Evaluate() int64 { return n.left.Evaluate() - n.right.Evaluate() }
func (n Multiply) Evaluate() int64 { return n.left.Evaluate() * n.right.Evaluate() }
func (n Divide) Evaluate() int64   { return n.left.Evaluate() / n.right.Evaluate() }

func operator(token string, left, right Node) Node {
	switch token {
	case "+":
		return &Add{left, right}
	case "-":
		return &Subtract{left, right}
	case "*":
		return &Multiply{left, right}
	}
	return &Divide{left, right}
}

type TreeBuilder struct{}

func (TreeBuilder) BuildTree(postfix []string) Node {
	stack := []Node{}
	for _, token := range postfix {
		if value, err := strconv.ParseInt(token, 10, 64); err == nil {
			stack = append(stack, &Number{value})
		} else {
			right := stack[len(stack)-1]
			left := stack[len(stack)-2]
			stack = stack[:len(stack)-2]
			stack = append(stack, operator(token, left, right))
		}
	}
	return stack[len(stack)-1]
}

func evaluatePostfix(postfix []string) int64 {
	builder := TreeBuilder{}
	tree := builder.BuildTree(postfix)
	return tree.Evaluate()
}

var seed int64 = 1628

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

func expression(leaves, top int64, tokens *[]string) int64 {
	if leaves == 1 {
		v := (nextRandom() * 32768 + nextRandom()) % top
		*tokens = append(*tokens, strconv.FormatInt(v, 10))
		return v
	}
	left := nextRandom()%(leaves-1) + 1
	a := expression(left, top, tokens)
	b := expression(leaves-left, top, tokens)
	op := []string{"+", "-", "*", "/"}[nextRandom()%4]
	if op == "/" && b == 0 {
		op = "*"
	}
	if op == "*" && abs(a*b) > 1000000000 {
		op = "+"
	}
	if op == "+" && abs(a+b) > 1000000000 {
		op = "-"
	}
	if op == "-" && abs(a-b) > 1000000000 {
		op = "+"
	}
	*tokens = append(*tokens, op)
	switch op {
	case "+":
		return a + b
	case "-":
		return a - b
	case "*":
		return a * b
	}
	return a / b
}

func main() {
	expressions := make([][]string, 20000)
	for i := range expressions {
		expression(50, 100001, &expressions[i])
	}
	var check, total int64
	for _, postfix := range expressions {
		got := evaluatePostfix(postfix)
		total += got
		check = ((check*31+got+1)%1000000007 + 1000000007) % 1000000007
	}
	fmt.Printf("20000 expressions of 50 operands: values sum to %d, checksum %d\n", total, check)
}
