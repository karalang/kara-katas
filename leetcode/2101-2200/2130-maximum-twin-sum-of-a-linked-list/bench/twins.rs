// LeetCode #2130: Maximum Twin Sum of a Linked List -- the benchmark, the
// same algorithm as twins.kara over `Option<Box<ListNode>>`.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn pair_sum(head: &Option<Box<ListNode>>) -> i64 {
    let mut values: Vec<i64> = Vec::new();
    let mut node = head;
    while let Some(n) = node {
        values.push(n.val);
        node = &n.next;
    }
    let len = values.len();
    let mut best = 0;
    for i in 0..len / 2 {
        best = best.max(values[i] + values[len - 1 - i]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 2130;
    let mut lists: Vec<Option<Box<ListNode>>> = Vec::new();
    for _ in 0..10 {
        let mut head: Option<Box<ListNode>> = None;
        for _ in 0..n {
            let v = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
            head = Some(Box::new(ListNode { val: v, next: head }));
        }
        lists.push(head);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..50i64 {
        for k in 0..10usize {
            let at = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let mut node = lists[k].as_mut().unwrap();
            for _ in 0..at {
                node = node.next.as_mut().unwrap();
            }
            node.val = next_random(&mut seed) % 200000 + 1;
            let sum = pair_sum(&lists[k]);
            total += sum;
            check = (check * 31 + sum + round) % 1000000007;
        }
    }
    println!("500 solves: {} in all, checksum {}", total, check);
    for list in lists.iter_mut() {
        let mut cur = list.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
    }
}
