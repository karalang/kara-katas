// Benchmark for #445: mirror of add_two_numbers.kara (two stacks) on 100
// random numbers of 1,000 to 2,000 digits, built once; 60 rounds add each
// to the next. Lists are `Option<Box<ListNode>>`, LeetCode's Rust shape.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

impl Drop for ListNode {
    // Unlink iteratively, so that dropping a long list does not recurse.
    fn drop(&mut self) {
        let mut next = self.next.take();
        while let Some(mut n) = next {
            next = n.next.take();
        }
    }
}

fn add_two_numbers(
    l1: &Option<Box<ListNode>>,
    l2: &Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    let mut a: Vec<i64> = Vec::new();
    let mut node = l1;
    while let Some(n) = node {
        a.push(n.val);
        node = &n.next;
    }
    let mut b: Vec<i64> = Vec::new();
    node = l2;
    while let Some(n) = node {
        b.push(n.val);
        node = &n.next;
    }
    let mut sum: Option<Box<ListNode>> = None;
    let mut carry = 0;
    while !a.is_empty() || !b.is_empty() || carry > 0 {
        let mut digit = carry;
        if let Some(d) = a.pop() {
            digit += d;
        }
        if let Some(d) = b.pop() {
            digit += d;
        }
        sum = Some(Box::new(ListNode {
            val: digit % 10,
            next: sum,
        }));
        carry = digit / 10;
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 60;
    let mut seed: i64 = 445;
    let mut numbers: Vec<Option<Box<ListNode>>> = Vec::new();
    for _ in 0..count {
        let length = 1000 + next_random(&mut seed) % 1001;
        let mut digits: Vec<i64> = Vec::new();
        for i in 0..length {
            let mut d = if next_random(&mut seed) % 2 == 0 {
                9
            } else {
                next_random(&mut seed) % 10
            };
            if i == 0 && d == 0 {
                d = 1;
            }
            digits.push(d);
        }
        let mut head: Option<Box<ListNode>> = None;
        for &d in digits.iter().rev() {
            head = Some(Box::new(ListNode { val: d, next: head }));
        }
        numbers.push(head);
    }
    let mut digits = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for i in 0..count {
            let sum = add_two_numbers(&numbers[i], &numbers[(i + 1) % count]);
            let mut node = &sum;
            while let Some(n) = node {
                digits += 1;
                checksum = (checksum * 31 + n.val + round) % 1000000007;
                node = &n.next;
            }
        }
    }
    println!("{rounds} rounds on {count} numbers: {digits} digits, checksum {checksum}");
}
