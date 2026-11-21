// LeetCode #1628: Design an Expression Tree With Evaluate Function -- the
// bench's Rust mirror: a Node trait, one struct per operator holding
// Box<dyn Node> operands, on 20000 random postfix expressions of 50
// operands, all drawn first.

trait Node {
    fn evaluate(&self) -> i64;
}

struct Number {
    value: i64,
}

struct Add {
    left: Box<dyn Node>,
    right: Box<dyn Node>,
}

struct Subtract {
    left: Box<dyn Node>,
    right: Box<dyn Node>,
}

struct Multiply {
    left: Box<dyn Node>,
    right: Box<dyn Node>,
}

struct Divide {
    left: Box<dyn Node>,
    right: Box<dyn Node>,
}

impl Node for Number {
    fn evaluate(&self) -> i64 {
        self.value
    }
}

impl Node for Add {
    fn evaluate(&self) -> i64 {
        self.left.evaluate() + self.right.evaluate()
    }
}

impl Node for Subtract {
    fn evaluate(&self) -> i64 {
        self.left.evaluate() - self.right.evaluate()
    }
}

impl Node for Multiply {
    fn evaluate(&self) -> i64 {
        self.left.evaluate() * self.right.evaluate()
    }
}

impl Node for Divide {
    fn evaluate(&self) -> i64 {
        self.left.evaluate() / self.right.evaluate()
    }
}

fn operator(token: &str, left: Box<dyn Node>, right: Box<dyn Node>) -> Box<dyn Node> {
    match token {
        "+" => Box::new(Add { left, right }),
        "-" => Box::new(Subtract { left, right }),
        "*" => Box::new(Multiply { left, right }),
        _ => Box::new(Divide { left, right }),
    }
}

struct TreeBuilder {}

impl TreeBuilder {
    fn build_tree(&self, postfix: &[String]) -> Box<dyn Node> {
        let mut stack: Vec<Box<dyn Node>> = Vec::new();
        for token in postfix {
            match token.parse::<i64>() {
                Ok(value) => stack.push(Box::new(Number { value })),
                Err(_) => {
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(operator(token, left, right));
                }
            }
        }
        stack.pop().unwrap()
    }
}

fn evaluate_postfix(postfix: &[String]) -> i64 {
    let builder = TreeBuilder {};
    let tree = builder.build_tree(postfix);
    tree.evaluate()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn expression(leaves: i64, top: i64, seed: &mut i64, tokens: &mut Vec<String>) -> i64 {
    if leaves == 1 {
        let v = (next_random(seed) * 32768 + next_random(seed)) % top;
        tokens.push(v.to_string());
        return v;
    }
    let left = next_random(seed) % (leaves - 1) + 1;
    let a = expression(left, top, seed, tokens);
    let b = expression(leaves - left, top, seed, tokens);
    let mut op = ["+", "-", "*", "/"][(next_random(seed) % 4) as usize];
    if op == "/" && b == 0 {
        op = "*";
    }
    if op == "*" && (a * b).abs() > 1000000000 {
        op = "+";
    }
    if op == "+" && (a + b).abs() > 1000000000 {
        op = "-";
    }
    if op == "-" && (a - b).abs() > 1000000000 {
        op = "+";
    }
    tokens.push(op.to_string());
    match op {
        "+" => a + b,
        "-" => a - b,
        "*" => a * b,
        _ => a / b,
    }
}

fn main() {
    let mut seed = 1628;
    let mut expressions: Vec<Vec<String>> = Vec::new();
    for _ in 0..20000 {
        let mut postfix = Vec::new();
        expression(50, 100001, &mut seed, &mut postfix);
        expressions.push(postfix);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for postfix in &expressions {
        let got = evaluate_postfix(postfix);
        total += got;
        check = ((check * 31 + got + 1) % 1000000007 + 1000000007) % 1000000007;
    }
    println!("20000 expressions of 50 operands: values sum to {}, checksum {}", total, check);
}
