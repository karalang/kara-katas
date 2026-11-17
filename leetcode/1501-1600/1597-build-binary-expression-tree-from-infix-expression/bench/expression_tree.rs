// LeetCode #1597: Build Binary Expression Tree From Infix Expression
// -- the bench in Rust, mirroring expression_tree.kara: two stacks, as
// the shunting-yard reads an expression, nodes as Rc<RefCell<Node>> (a
// Kāra `shared struct` is counted the same way), on 200000 expressions of
// up to 50 digits, all drawn first, each tree folded to a hash.

use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    val: char,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
}

fn leaf(val: char) -> Rc<RefCell<Node>> {
    Rc::new(RefCell::new(Node { val, left: None, right: None }))
}

fn precedence(op: char) -> i64 {
    match op {
        '+' | '-' => 1,
        '*' | '/' => 2,
        _ => 0,
    }
}

fn join(ops: &mut Vec<char>, trees: &mut Vec<Rc<RefCell<Node>>>) {
    let op = ops.pop().unwrap();
    let right = trees.pop().unwrap();
    let left = trees.pop().unwrap();
    trees.push(Rc::new(RefCell::new(Node { val: op, left: Some(left), right: Some(right) })));
}

fn exp_tree(s: &str) -> Option<Rc<RefCell<Node>>> {
    let mut ops: Vec<char> = Vec::new();
    let mut trees: Vec<Rc<RefCell<Node>>> = Vec::new();
    for c in s.chars() {
        if c.is_ascii_digit() {
            trees.push(leaf(c));
        } else if c == '(' {
            ops.push(c);
        } else if c == ')' {
            while ops.last() != Some(&'(') {
                join(&mut ops, &mut trees);
            }
            ops.pop();
        } else {
            while ops.last().is_some_and(|top| precedence(*top) >= precedence(c)) {
                join(&mut ops, &mut trees);
            }
            ops.push(c);
        }
    }
    while !ops.is_empty() {
        join(&mut ops, &mut trees);
    }
    trees.pop()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn expression(operands: i64, seed: &mut i64) -> String {
    if operands <= 1 || next_random(seed) % 4 == 0 {
        return format!("{}", next_random(seed) % 10);
    }
    let left = next_random(seed) % (operands - 1) + 1;
    let op = ["+", "-", "*", "/"][(next_random(seed) % 4) as usize];
    let a = expression(left, seed);
    let b = expression(operands - left, seed);
    let body = format!("{}{}{}", a, op, b);
    if next_random(seed) % 4 == 0 { format!("({})", body) } else { body }
}

fn fold(tree: &Rc<RefCell<Node>>) -> i64 {
    let n = tree.borrow();
    let left = match &n.left { Some(l) => fold(l), None => 7 };
    let right = match &n.right { Some(r) => fold(r), None => 11 };
    ((n.val as i64) * 1000003 + left * 31 + right * 17) % 1000000007
}

fn main() {
    let mut seed = 1597;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..200000 {
        let operands = next_random(&mut seed) % 50 + 1;
        texts.push(expression(operands, &mut seed));
    }
    let mut check: i64 = 0;
    let mut length = 0;
    for s in &texts {
        length += s.len();
        let tree = exp_tree(s).unwrap();
        check = (check * 31 + fold(&tree)) % 1000000007;
    }
    println!("200000 expressions, {} characters: checksum {}", length, check);
}
