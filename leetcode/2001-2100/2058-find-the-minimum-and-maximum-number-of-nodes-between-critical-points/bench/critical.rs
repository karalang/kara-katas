// LeetCode #2058: Find the Minimum and Maximum Number of Nodes Between
// Critical Points -- Rust mirror of the ★ arm's benchmark (critical.kara):
// the same 50 lists of 100000 values, each built node by node as
// `Option<Box<ListNode>>` and answered by one walk.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn nodes_between_critical_points(head: &Option<Box<ListNode>>) -> [i64; 2] {
    let Some(first_node) = head else {
        return [-1, -1];
    };
    let mut before = first_node.val;
    let mut cur = &first_node.next;
    let mut at = 1;
    let (mut first, mut last, mut nearest) = (-1i64, -1i64, -1i64);
    while let Some(node) = cur {
        if let Some(after) = &node.next {
            let v = node.val;
            if (v > before && v > after.val) || (v < before && v < after.val) {
                if first < 0 {
                    first = at;
                } else if nearest < 0 || at - last < nearest {
                    nearest = at - last;
                }
                last = at;
            }
        }
        before = node.val;
        cur = &node.next;
        at += 1;
    }
    if nearest < 0 { [-1, -1] } else { [nearest, last - first] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let tops = [2i64, 3, 10, 100000];
    let mut seed: i64 = 2058;
    let (mut total, mut check) = (0i64, 0i64);
    for t in 0..50 {
        let top = tops[t % 4];
        let mut head: Option<Box<ListNode>> = None;
        for _ in 0..100000 {
            head = Some(Box::new(ListNode { val: next_random(&mut seed) % top + 1, next: head }));
        }
        let d = nodes_between_critical_points(&head);
        // unlink iteratively, as the Kāra and C programs free the list
        let mut cur = head;
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
        total += d[0] + d[1];
        check = (check * 31 + d[0] + 2) % 1000000007;
        check = (check * 31 + d[1] + 2) % 1000000007;
    }
    println!("50 lists: sum {total}, checksum {check}");
}
