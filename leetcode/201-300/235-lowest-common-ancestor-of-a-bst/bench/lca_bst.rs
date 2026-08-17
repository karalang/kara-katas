// Benchmark harness for LeetCode #235 — Lowest Common Ancestor of a BST.
// Mirrors lca_bst.kara algorithm-for-algorithm, including the index-pool tree
// (parallel Vec of nodes with i64 child indices, -1 = null) rather than
// Box/Rc-linked nodes, so pointer-chasing behaviour matches.

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn lca(nodes: &[Node], root: i64, p: i64, q: i64) -> i64 {
    let mut cur = root;
    while cur != -1 {
        let v = nodes[cur as usize].val;
        if p < v && q < v {
            cur = nodes[cur as usize].left;
        } else if p > v && q > v {
            cur = nodes[cur as usize].right;
        } else {
            return v;
        }
    }
    -1
}

fn main() {
    let n: i64 = 200000;
    let iters: i64 = 8000000;

    let mut vals: Vec<i64> = Vec::new();
    let mut x: i64 = 7;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        let hi = x / 65536;
        x = (x * 1103515245 + 12345) % 2147483648;
        vals.push((hi * 32768 + x / 65536) % 1000000);
    }

    let mut nodes: Vec<Node> = Vec::new();
    let mut root: i64 = -1;
    for b in 0..n {
        let v = vals[b as usize];
        if root == -1 {
            nodes.push(Node {
                val: v,
                left: -1,
                right: -1,
            });
            root = 0;
        } else {
            let mut cur = root;
            loop {
                if v < nodes[cur as usize].val {
                    let l = nodes[cur as usize].left;
                    if l == -1 {
                        let idx = nodes.len() as i64;
                        nodes.push(Node {
                            val: v,
                            left: -1,
                            right: -1,
                        });
                        nodes[cur as usize].left = idx;
                        break;
                    }
                    cur = l;
                } else {
                    let r = nodes[cur as usize].right;
                    if r == -1 {
                        let idx = nodes.len() as i64;
                        nodes.push(Node {
                            val: v,
                            left: -1,
                            right: -1,
                        });
                        nodes[cur as usize].right = idx;
                        break;
                    }
                    cur = r;
                }
            }
        }
    }

    let mut sink: i64 = 0;
    let mut y: i64 = 99;
    for _ in 0..iters {
        y = (y * 1103515245 + 12345) % 2147483648;
        let phi = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648;
        let pi = ((phi * 32768 + y / 65536) % n) as usize;
        y = (y * 1103515245 + 12345) % 2147483648;
        let qhi = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648;
        let qi = ((qhi * 32768 + y / 65536) % n) as usize;
        let a = lca(&nodes, root, vals[pi], vals[qi]);
        sink = (sink + a) % 1000000007;
    }
    println!("{}", sink);
}
