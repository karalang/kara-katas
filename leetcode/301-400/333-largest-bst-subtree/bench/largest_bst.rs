// Benchmark workload for LeetCode #333 — Rust mirror of largest_bst.kara.

const NODES: i64 = 100000;
const PUNCHES: i64 = 200;
const MODULUS: i64 = 1073741789;

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

struct Info {
    bst: bool,
    size: i64,
    lo: i64,
    hi: i64,
}

fn visit(nodes: &[Node], node: i64, best: &mut i64) -> Info {
    let val = nodes[node as usize].val;
    let left = nodes[node as usize].left;
    let right = nodes[node as usize].right;
    let mut bst = true;
    let mut size = 1;
    let mut lo = val;
    let mut hi = val;
    if left != -1 {
        let l = visit(nodes, left, best);
        if l.bst && l.hi < val {
            size += l.size;
            lo = l.lo;
        } else {
            bst = false;
        }
    }
    if right != -1 {
        let r = visit(nodes, right, best);
        if r.bst && r.lo > val {
            size += r.size;
            hi = r.hi;
        } else {
            bst = false;
        }
    }
    if bst && size > *best {
        *best = size;
    }
    Info { bst, size, lo, hi }
}

fn largest_bst_subtree(nodes: &[Node]) -> i64 {
    if nodes.is_empty() {
        return 0;
    }
    let mut best = 0;
    let _ = visit(nodes, 0, &mut best);
    best
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next(seed);
    hi * 32768 + next(seed)
}

fn insert(nodes: &mut Vec<Node>, v: i64) {
    nodes.push(Node { val: v, left: -1, right: -1 });
    let id = nodes.len() as i64 - 1;
    let mut cur = 0i64;
    while cur != id {
        let c = cur as usize;
        if v < nodes[c].val {
            if nodes[c].left == -1 {
                nodes[c].left = id;
            }
            cur = nodes[c].left;
        } else {
            if nodes[c].right == -1 {
                nodes[c].right = id;
            }
            cur = nodes[c].right;
        }
    }
}

fn main() {
    let mut seed = 333i64;
    let mut vals: Vec<i64> = (0..NODES).map(|i| i * 2).collect();
    for i in 0..NODES {
        let j = i + wide(&mut seed) % (NODES - i);
        vals.swap(i as usize, j as usize);
    }
    let mut nodes: Vec<Node> = Vec::new();
    for &v in &vals {
        insert(&mut nodes, v);
    }
    let mut sink = 0i64;
    for _ in 0..PUNCHES {
        let at = (wide(&mut seed) % NODES) as usize;
        let old = nodes[at].val;
        nodes[at].val = wide(&mut seed) % (2 * NODES);
        let answer = largest_bst_subtree(&nodes);
        nodes[at].val = old;
        sink = (sink * 1000003 + answer) % MODULUS;
    }
    println!("{sink}");
}
