// Benchmark workload for LeetCode #337 — Rust mirror of house_robber_iii.kara.

const HOUSES: i64 = 500000;
const PUNCHES: i64 = 100;
const MODULUS: i64 = 1073741789;

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn visit(nodes: &[Node], node: i64) -> (i64, i64) {
    if node == -1 {
        return (0, 0);
    }
    let n = &nodes[node as usize];
    let (lr, ls) = visit(nodes, n.left);
    let (rr, rs) = visit(nodes, n.right);
    (n.val + ls + rs, lr.max(ls) + rr.max(rs))
}

fn rob(nodes: &[Node]) -> i64 {
    if nodes.is_empty() {
        return 0;
    }
    let (r, s) = visit(nodes, 0);
    r.max(s)
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next(seed);
    hi * 32768 + next(seed)
}

fn main() {
    let mut seed = 337;
    let mut nodes: Vec<Node> = Vec::new();
    for i in 0..HOUSES {
        nodes.push(Node { val: next(&mut seed) % 10001, left: -1, right: -1 });
        if i == 0 {
            continue;
        }
        let mut cur = 0usize;
        loop {
            if next(&mut seed) % 2 == 0 {
                if nodes[cur].left == -1 {
                    nodes[cur].left = i;
                    break;
                }
                cur = nodes[cur].left as usize;
            } else {
                if nodes[cur].right == -1 {
                    nodes[cur].right = i;
                    break;
                }
                cur = nodes[cur].right as usize;
            }
        }
    }
    let mut sink = 0;
    for _ in 0..PUNCHES {
        let at = (wide(&mut seed) % HOUSES) as usize;
        let old = nodes[at].val;
        nodes[at].val = next(&mut seed) % 10001;
        let answer = rob(&nodes);
        nodes[at].val = old;
        sink = (sink * 1000003 + answer) % MODULUS;
    }
    println!("{}", sink);
}
