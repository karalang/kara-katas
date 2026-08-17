// Benchmark harness for LeetCode #236 — LCA of a Binary Tree.
// Mirrors lca_binary_tree.kara algorithm-for-algorithm, including the index-pool
// tree and the recursive post-order search.

struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn lca(nodes: &[Node], cur: i64, p: i64, q: i64) -> i64 {
    if cur == -1 {
        return -1;
    }
    if nodes[cur as usize].val == p || nodes[cur as usize].val == q {
        return cur;
    }
    let l = lca(nodes, nodes[cur as usize].left, p, q);
    let r = lca(nodes, nodes[cur as usize].right, p, q);
    if l != -1 && r != -1 {
        return cur;
    }
    if l != -1 {
        return l;
    }
    r
}

fn main() {
    let n: i64 = 100000;
    let iters: i64 = 600;

    let mut nodes: Vec<Node> = Vec::new();
    for i in 0..n {
        let lc = 2 * i + 1;
        let rc = 2 * i + 2;
        nodes.push(Node {
            val: i,
            left: if lc < n { lc } else { -1 },
            right: if rc < n { rc } else { -1 },
        });
    }

    let mut sink: i64 = 0;
    let mut y: i64 = 2024;
    for _ in 0..iters {
        y = (y * 1103515245 + 12345) % 2147483648;
        let wd1 = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648;
        let p = (wd1 * 32768 + y / 65536) % n;
        y = (y * 1103515245 + 12345) % 2147483648;
        let wd0 = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648;
        let q = (wd0 * 32768 + y / 65536) % n;
        let ans = lca(&nodes, 0, p, q);
        let v = if ans == -1 { -1 } else { nodes[ans as usize].val };
        sink = (sink + v) % 1000000007;
    }
    println!("{}", sink);
}
