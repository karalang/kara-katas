// LeetCode #2816: Double a Number Represented as a Linked List -- the
// bench in Rust: the ★ arm over 200 numbers of 10^4 digits, all drawn
// first, then each built as a list and doubled 20 times, the list read
// back after each. The list is LeetCode's `Option<Box<ListNode>>`.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn double_it(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut head = head?;
    if head.val > 4 {
        head = Box::new(ListNode { val: 0, next: Some(head) });
    }
    let mut cur = Some(&mut head);
    while let Some(node) = cur {
        node.val = node.val * 2 % 10;
        if let Some(after) = &node.next {
            if after.val > 4 {
                node.val += 1;
            }
        }
        cur = node.next.as_mut();
    }
    Some(head)
}

fn build(values: &[i64]) -> Option<Box<ListNode>> {
    let mut head: Option<Box<ListNode>> = None;
    for &v in values.iter().rev() {
        head = Some(Box::new(ListNode { val: v, next: head }));
    }
    head
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 200;
    let rounds = 20;
    let n = 10000;
    let mut rng = Rng(2816);
    let mut numbers: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut digits: Vec<i64> = (0..n).map(|_| rng.next_random() % 10).collect();
        if digits[0] == 0 {
            digits[0] = rng.next_random() % 9 + 1;
        }
        numbers.push(digits);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for digits in &numbers {
            let list = double_it(build(digits));
            let mut h = r;
            let mut cur = list.as_deref();
            while let Some(node) = cur {
                total += node.val;
                h = (h * 131 + node.val) % 1000000007;
                cur = node.next.as_deref();
            }
            check = (check * 31 + h) % 1000000007;
        }
    }
    println!("{count} numbers of {n} digits, {rounds} rounds: digits sum to {total}, checksum {check}");
}
