// Benchmark: LeetCode #1006 Clumsy Factorial -- the ★ arm, a stack, on
// every n up to 10000, LeetCode's largest.
// Mirrors clumsy.kara, .c, .py and go-seq/.

fn clumsy(n: i64) -> i64 {
    let mut stack: Vec<i64> = vec![n];
    let mut op = 0;
    let mut x = n - 1;
    while x > 0 {
        let last = stack.len() - 1;
        if op == 0 {
            stack[last] *= x;
        } else if op == 1 {
            stack[last] /= x;
        } else if op == 2 {
            stack.push(x);
        } else {
            stack.push(-x);
        }
        op = (op + 1) % 4;
        x -= 1;
    }
    stack.iter().sum()
}

fn main() {
    let rounds: i64 = 4;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..10000i64 {
            let n = if r % 2 == 0 { i + 1 } else { 10000 - i };
            let got = clumsy(n);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("{rounds} rounds over every n up to 10000: answers sum to {total}, checksum {check}");
}
