// LeetCode #1290 bench: the ★ arm over 10^4 lists of 30 nodes built once,
// then 500 passes, each setting one bit of every list and reading it back.
// The list is LeetCode's Rust `ListNode`, each node in its own `Box`.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn get_decimal_value(head: &Option<Box<ListNode>>) -> i64 {
    let mut value = 0;
    let mut cur = head;
    while let Some(node) = cur {
        value = value * 2 + node.val;
        cur = &node.next;
    }
    value
}

fn set_bit(head: &mut Option<Box<ListNode>>, k: i64, bit: i64) {
    let mut cur = head;
    let mut i = 0;
    while let Some(node) = cur {
        if i == k {
            node.val = bit;
            return;
        }
        i += 1;
        cur = &mut node.next;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1290;
    let mut heads: Vec<Option<Box<ListNode>>> = Vec::new();
    for _ in 0..10000 {
        let mut head: Option<Box<ListNode>> = None;
        for _ in 0..30 {
            head = Some(Box::new(ListNode { val: next_random(&mut seed) % 2, next: head }));
        }
        heads.push(head);
    }
    let mut check: i64 = 0;
    for p in 0..500 {
        for a in 0..heads.len() {
            set_bit(&mut heads[a], (check + a as i64) % 30, check / 16 % 2);
            check = (check * 31 + get_decimal_value(&heads[a]) + p) % 1000000007;
        }
    }
    println!("500 passes over 10^4 lists of 30 bits: checksum {}", check);
}
