// Benchmark for #817: Linked List Components -- mirror of the ★ arm (count
// the ends), with the same workload as linked_list_components.kara. The
// list is `Option<Box<ListNode>>`, LeetCode's Rust signature.
use std::collections::HashSet;

struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

fn num_components(head: &Option<Box<ListNode>>, nums: &[i64]) -> i64 {
    let wanted: HashSet<i64> = nums.iter().copied().collect();
    let mut count = 0;
    let mut cur = head;
    while let Some(node) = cur {
        if wanted.contains(&node.val) {
            let ends = match &node.next {
                Some(next) => !wanted.contains(&next.val),
                None => true,
            };
            if ends {
                count += 1;
            }
        }
        cur = &node.next;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let n: i64 = 10000;
    let rounds: i64 = 8000;
    let mut seed: i64 = 817;
    let mut lists: Vec<Option<Box<ListNode>>> = Vec::new();
    let mut inside: Vec<Vec<i64>> = Vec::new();
    let mut outside: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut order: Vec<i64> = (0..n).collect();
        for i in 0..n {
            let j = i + next_random(&mut seed) % (n - i);
            order.swap(i as usize, j as usize);
        }
        let mut head: Option<Box<ListNode>> = None;
        for k in 0..n {
            head = Some(Box::new(ListNode {
                val: order[(n - 1 - k) as usize],
                next: head,
            }));
        }
        lists.push(head);
        for i in 0..n {
            let j = i + next_random(&mut seed) % (n - i);
            order.swap(i as usize, j as usize);
        }
        let m = (1 + next_random(&mut seed) % (n - 1)) as usize;
        inside.push(order[..m].to_vec());
        outside.push(order[m..].to_vec());
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = (round % count as i64) as usize;
        let a = (next_random(&mut seed) % inside[g].len() as i64) as usize;
        let b = (next_random(&mut seed) % outside[g].len() as i64) as usize;
        std::mem::swap(&mut inside[g][a], &mut outside[g][b]);
        let answer = num_components(&lists[g], &inside[g]);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!(
        "{} rounds of {} nodes: total {}, checksum {}",
        rounds, n, total, checksum
    );
    // A long Box chain would overflow the stack in its recursive drop.
    for head in lists.iter_mut() {
        let mut cur = head.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
    }
}
