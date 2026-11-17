// LeetCode #1597: Build Binary Expression Tree From Infix Expression
// -- the bench in Go, mirroring expression_tree.kara: two stacks, as the
// shunting-yard reads an expression, on 200000 expressions of up to 50
// digits, all drawn first, each tree folded to a hash.
package main

import (
	"fmt"
	"strconv"
)

type Node struct {
	val         byte
	left, right *Node
}

func precedence(op byte) int {
	switch op {
	case '+', '-':
		return 1
	case '*', '/':
		return 2
	}
	return 0
}

func join(ops *[]byte, trees *[]*Node) {
	op := (*ops)[len(*ops)-1]
	*ops = (*ops)[:len(*ops)-1]
	right := (*trees)[len(*trees)-1]
	left := (*trees)[len(*trees)-2]
	*trees = (*trees)[:len(*trees)-2]
	*trees = append(*trees, &Node{op, left, right})
}

func expTree(s string) *Node {
	var ops []byte
	var trees []*Node
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= '0' && c <= '9' {
			trees = append(trees, &Node{val: c})
		} else if c == '(' {
			ops = append(ops, c)
		} else if c == ')' {
			for ops[len(ops)-1] != '(' {
				join(&ops, &trees)
			}
			ops = ops[:len(ops)-1]
		} else {
			for len(ops) > 0 && precedence(ops[len(ops)-1]) >= precedence(c) {
				join(&ops, &trees)
			}
			ops = append(ops, c)
		}
	}
	for len(ops) > 0 {
		join(&ops, &trees)
	}
	return trees[len(trees)-1]
}

var seed int64 = 1597

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func expression(operands int64) string {
	if operands <= 1 || nextRandom()%4 == 0 {
		return strconv.FormatInt(nextRandom()%10, 10)
	}
	left := nextRandom()%(operands-1) + 1
	op := "+-*/"[nextRandom()%4]
	a := expression(left)
	b := expression(operands - left)
	body := a + string(op) + b
	if nextRandom()%4 == 0 {
		return "(" + body + ")"
	}
	return body
}

func fold(n *Node) int64 {
	var left, right int64 = 7, 11
	if n.left != nil {
		left = fold(n.left)
	}
	if n.right != nil {
		right = fold(n.right)
	}
	return (int64(n.val)*1000003 + left*31 + right*17) % 1000000007
}

func main() {
	texts := make([]string, 200000)
	for i := range texts {
		operands := nextRandom()%50 + 1
		texts[i] = expression(operands)
	}
	var check, length int64
	for _, s := range texts {
		length += int64(len(s))
		check = (check*31 + fold(expTree(s))) % 1000000007
	}
	fmt.Printf("200000 expressions, %d characters: checksum %d\n", length, check)
}
