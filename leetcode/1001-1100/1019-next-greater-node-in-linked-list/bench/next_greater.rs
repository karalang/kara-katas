// LeetCode #1019: Next Greater Node In Linked List -- bench
// Mirrors next_greater.kara with `Option<Box<ListNode>>`, LeetCode's Rust
// signature, walked by reference. See ../README.md § Benchmarks.

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn next_larger_nodes(head: &Option<Box<ListNode>>) -> Vec<i64> {
    let mut values: Vec<i64> = Vec::new();
    let mut answer: Vec<i64> = Vec::new();
    let mut waiting: Vec<usize> = Vec::new();
    let mut cur = head;
    while let Some(node) = cur {
        let v = node.val;
        while let Some(&w) = waiting.last() {
            if values[w] >= v {
                break;
            }
            answer[w] = v;
            waiting.pop();
        }
        waiting.push(values.len());
        values.push(v);
        answer.push(0);
        cur = &node.next;
    }
    answer
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
    let count: i64 = 500;
    let rounds: i64 = 10;
    let mut seed: i64 = 1019;
    let mut lists: Vec<Option<Box<ListNode>>> = Vec::new();
    let mut nodes: i64 = 0;
    for _ in 0..count {
        let len = next_random(&mut seed) % 10000 + 1;
        let mut values: Vec<i64> = Vec::new();
        for _ in 0..len {
            let hi = next_random(&mut seed);
            values.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
        }
        nodes += len;
        lists.push(from_values(&values));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for head in lists.iter() {
            for a in next_larger_nodes(head) {
                total = (total + a) % 1000000007;
                check = (check * 31 + a) % 1000000007;
            }
        }
    }
    println!("{} lists, {} nodes, {} rounds: answer sum {}, checksum {}", count, nodes, rounds, total, check);
}
