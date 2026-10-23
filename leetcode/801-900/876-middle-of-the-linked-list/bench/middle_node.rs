// LeetCode #876 bench: Rust mirror of middle_node.kara (the ★ arm, slow
// and fast pointers) on the same 2,000,000 searches. The list is
// `Option<Box<ListNode>>`, LeetCode's Rust signature, walked by reference.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn middle_node(head: &Option<Box<ListNode>>) -> &Option<Box<ListNode>> {
    let mut slow = head;
    let mut fast = head;
    while let Some(f) = fast {
        let Some(after) = &f.next else {
            break;
        };
        fast = &after.next;
        if let Some(s) = slow {
            slow = &s.next;
        }
    }
    slow
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn from_values(values: &[i64]) -> Option<Box<ListNode>> {
    let mut head: Option<Box<ListNode>> = None;
    for &v in values.iter().rev() {
        head = Some(Box::new(ListNode { val: v, next: head }));
    }
    head
}

fn main() {
    let mut seed: i64 = 876;
    let mut lists: Vec<Option<Box<ListNode>>> = Vec::new();
    for _ in 0..2000 {
        let n = next_random(&mut seed) % 100 + 1;
        let mut values = Vec::new();
        for _ in 0..n {
            values.push(next_random(&mut seed) % 100 + 1);
        }
        lists.push(from_values(&values));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for k in 0..2000000usize {
        if let Some(m) = middle_node(&lists[(k * 7 + k / 2000) % 2000]) {
            total += m.val;
            check = (check * 131 + m.val) % 1000000007;
        }
    }
    println!("2000000 searches over 2000 lists: middle values sum to {}, checksum {}", total, check);
}
