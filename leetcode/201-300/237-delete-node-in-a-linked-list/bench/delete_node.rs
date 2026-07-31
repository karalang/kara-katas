// Benchmark workload for LeetCode #237 — Delete Node in a Linked List (Rust mirror).
#[derive(Clone, Copy)]
struct Node {
    val: i64,
    next: i64,
}

fn main() {
    let n: i64 = 8000;
    let cycles: i64 = 7000;
    let mut nodes = vec![Node { val: 0, next: -1 }; n as usize];
    let mut state: i64 = 12345;
    for i in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        nodes[i].val = state % 50;
        nodes[i].next = -1;
    }

    let mut sink: i64 = 0;
    for _ in 0..cycles {
        for r in 0..n {
            nodes[r as usize].next = if r + 1 < n { r + 1 } else { -1 };
        }
        while nodes[0].next != -1 {
            let mut cur: i64 = 0;
            while cur != -1 && nodes[cur as usize].next != -1 {
                let s = nodes[cur as usize].next;
                nodes[cur as usize].val = nodes[s as usize].val;
                nodes[cur as usize].next = nodes[s as usize].next;
                cur = nodes[cur as usize].next;
            }
            let mut pass: i64 = 0;
            let mut k: i64 = 0;
            while k != -1 {
                pass += nodes[k as usize].val;
                k = nodes[k as usize].next;
            }
            sink = (sink * 31 + pass) & 1073741823;
        }
    }
    println!("{}", sink);
}
