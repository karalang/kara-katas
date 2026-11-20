// LeetCode #1721: Swapping Nodes in a Linked List -- the bench
// (swap.kara): the kth node found, then a runner from it to the last node
// drags a second cursor from the head to the kth node from the end.
//
// The list is a vector of nodes linked by index, Rust's usual way to hold
// a list it walks from the middle: `Option<Box<ListNode>>` gives no second
// cursor into a list the first one is in.

struct Node {
    val: i64,
    next: Option<usize>,
}

fn swap_nodes(nodes: &mut [Node], head: usize, k: i64) -> usize {
    let mut first = head;
    for _ in 1..k {
        first = nodes[first].next.unwrap();
    }
    let mut second = head;
    let mut runner = first;
    while let Some(next) = nodes[runner].next {
        runner = next;
        second = nodes[second].next.unwrap();
    }
    let value = nodes[first].val;
    nodes[first].val = nodes[second].val;
    nodes[second].val = value;
    head
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds: i64 = 100;
    let n: i64 = 100000;
    let mut seed: i64 = 1721;
    let mut lists: Vec<Vec<Node>> = Vec::new();
    for _ in 0..count {
        let values: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % 101).collect();
        let nodes: Vec<Node> = values
            .iter()
            .enumerate()
            .map(|(i, &v)| Node { val: v, next: if (i as i64) + 1 < n { Some(i + 1) } else { None } })
            .collect();
        lists.push(nodes);
    }
    let ks: Vec<i64> = (0..count * rounds).map(|_| wide(&mut seed) % n + 1).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            let head = swap_nodes(&mut lists[c], 0, ks[(r * count + c as i64) as usize]);
            let v = lists[c][head].val;
            sum += v;
            check = (check * 31 + v + r) % 1000000007;
        }
    }
    println!("{} lists of {} nodes, {} rounds: heads sum to {}, checksum {}", count, n, rounds, sum, check);
}
