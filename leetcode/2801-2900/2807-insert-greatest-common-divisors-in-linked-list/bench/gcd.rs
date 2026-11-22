// LeetCode #2807: Insert Greatest Common Divisors in Linked List -- the
// bench in Rust: the ★ arm over 200 lists of 5000 values up to 1000, all
// drawn first, then each built afresh and answered 10 times; the list is
// LeetCode's `Option<Box<ListNode>>`, walked by `as_mut` and `take`.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

fn insert_greatest_common_divisors(mut head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut cur = head.as_mut();
    while let Some(node) = cur {
        match node.next.take() {
            Some(after) => {
                let g = gcd(node.val, after.val);
                node.next = Some(Box::new(ListNode { val: g, next: Some(after) }));
                cur = node.next.as_mut().unwrap().next.as_mut();
            }
            None => break,
        }
    }
    head
}

fn build(values: &[i64]) -> Option<Box<ListNode>> {
    let mut head = None;
    for &v in values.iter().rev() {
        head = Some(Box::new(ListNode { val: v, next: head }));
    }
    head
}

fn free(mut head: Option<Box<ListNode>>) {
    while let Some(mut node) = head {
        head = node.next.take();
    }
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
    let rounds = 10;
    let mut rng = Rng(2807);
    let mut cases = Vec::new();
    for t in 0..count {
        let step = if t % 2 == 0 { 12 } else { 1 };
        let values: Vec<i64> = (0..5000).map(|_| (rng.next_random() % (1000 / step) + 1) * step).collect();
        cases.push(values);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for values in &cases {
            let head = insert_greatest_common_divisors(build(values));
            let mut sum = 0;
            let mut cur = head.as_ref();
            while let Some(node) = cur {
                sum += node.val;
                cur = node.next.as_ref();
            }
            free(head);
            total += sum;
            check = (check * 31 + sum + r) % 1000000007;
        }
    }
    println!("{count} lists of 5000, {rounds} rounds: values sum to {total}, checksum {check}");
}
