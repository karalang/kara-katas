// Benchmark lane for LeetCode 314 — Rust mirror of bench/vertical.kara.
// Grow POOL random trees of NODES Box nodes once, then PASSES vertical-order
// traversals (extent pass + level-frontier BFS into an offset-indexed
// Vec<Vec<i64>>), each on the tree the running checksum selects. Every column's
// length and every value is folded into the masked checksum.

const POOL: i64 = 8;
const NODES: i64 = 50000;
const PASSES: i64 = 240;
const MASK: i64 = 1073741823;

struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn lcg(s: i64) -> i64 {
    (s * 1103515245 + 12345) & 0x7fffffff
}

fn grow(n: i64, seed: &mut i64) -> Option<Box<Node>> {
    if n <= 0 {
        return None;
    }
    *seed = lcg(*seed);
    let v = *seed % 1000 - 500;
    *seed = lcg(*seed);
    let left_n = if n <= 1 { 0 } else { *seed % n };
    let right_n = n - 1 - left_n;
    let l = grow(left_n, seed);
    let r = grow(right_n, seed);
    Some(Box::new(Node { val: v, left: l, right: r }))
}

fn extent(t: &Option<Box<Node>>, col: i64, lo: &mut i64, hi: &mut i64) {
    if let Some(n) = t {
        if col < *lo {
            *lo = col;
        }
        if col > *hi {
            *hi = col;
        }
        extent(&n.left, col - 1, lo, hi);
        extent(&n.right, col + 1, lo, hi);
    }
}

fn vertical_order(root: &Option<Box<Node>>) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<(&Node, i64)> = Vec::new();
    match root {
        None => return out,
        Some(n) => current.push((n, 0)),
    }
    let mut lo = 0;
    let mut hi = 0;
    extent(root, 0, &mut lo, &mut hi);
    for _ in lo..(hi + 1) {
        out.push(Vec::new());
    }
    while !current.is_empty() {
        let mut next: Vec<(&Node, i64)> = Vec::new();
        for (n, c) in current {
            out[(c - lo) as usize].push(n.val);
            if let Some(l) = &n.left {
                next.push((l, c - 1));
            }
            if let Some(r) = &n.right {
                next.push((r, c + 1));
            }
        }
        current = next;
    }
    out
}

fn main() {
    let mut seed: i64 = 314159;
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for _ in 0..POOL {
        pool.push(grow(NODES, &mut seed));
    }

    let mut checksum: i64 = 0;
    for _ in 0..PASSES {
        let which = (checksum % POOL) as usize;
        let cols = vertical_order(&pool[which]);
        checksum = (checksum + cols.len() as i64) & MASK;
        for col in &cols {
            checksum = (checksum * 31 + col.len() as i64) & MASK;
            for &v in col {
                checksum = (checksum + v + 500) & MASK;
            }
        }
    }
    println!("checksum {}", checksum);
}
