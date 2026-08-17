// Benchmark workload for LeetCode #257 — Binary Tree Paths (Rust mirror).
// Mirrors binary_tree_paths.kara algorithm-for-algorithm: same LCG, same bushy
// tree construction, same string-extending DFS, same positional digest.

struct Node { val: i64, left: i64, right: i64 }

fn walk(nodes: &Vec<Node>, node: usize, prefix: &str, out: &mut Vec<String>) {
    let (left, right) = (nodes[node].left, nodes[node].right);
    if left == -1 && right == -1 {
        out.push(prefix.to_string());
        return;
    }
    if left != -1 {
        let mut next = String::with_capacity(prefix.len() + 8);
        next.push_str(prefix);
        next.push_str("->");
        next.push_str(&format!("{}", nodes[left as usize].val));
        walk(nodes, left as usize, &next, out);
    }
    if right != -1 {
        let mut next = String::with_capacity(prefix.len() + 8);
        next.push_str(prefix);
        next.push_str("->");
        next.push_str(&format!("{}", nodes[right as usize].val));
        walk(nodes, right as usize, &next, out);
    }
}

fn main() {
    let n: i64 = 150000;
    let rounds: i64 = 5;

    let mut nodes: Vec<Node> = Vec::new();
    let mut open: Vec<i64> = Vec::new();
    let mut state: i64 = 257257;
    state = (state * 1103515245 + 12345) & 2147483647;
    nodes.push(Node { val: (state / 65536) % 100 - 50, left: -1, right: -1 });
    open.push(0);

    let mut made: i64 = 1;
    while made < n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let wd0 = state / 65536;
        state = (state * 1103515245 + 12345) & 2147483647;
        let pick = ((wd0 * 32768 + state / 65536) % open.len() as i64) as usize;
        let parent = open[pick] as usize;
        state = (state * 1103515245 + 12345) & 2147483647;
        nodes.push(Node { val: (state / 65536) % 100 - 50, left: -1, right: -1 });
        let child = nodes.len() as i64 - 1;
        if nodes[parent].left == -1 {
            nodes[parent].left = child;
        } else {
            nodes[parent].right = child;
            let last = open[open.len() - 1];
            open[pick] = last;
            open.pop();
        }
        open.push(child);
        made += 1;
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let mut out: Vec<String> = Vec::new();
        let root_s = format!("{}", nodes[0].val);
        walk(&nodes, 0, &root_s, &mut out);

        let mut h: i64 = 1;
        for s in &out {
            for &b in s.as_bytes() {
                h = (h * 1000003 + b as i64) % 1000000007;
            }
            h = (h * 31 + 7) % 1000000007;
        }
        sink = (sink * 131 + h) % 1000000007;
    }
    println!("{}", sink);
}
