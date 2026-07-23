struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn build(n: i64) -> Vec<Node> {
    let mut nodes: Vec<Node> = Vec::with_capacity(n as usize);
    for i in 0..n {
        let l = 2 * i + 1;
        let r = 2 * i + 2;
        nodes.push(Node {
            val: i,
            left: if l < n { l } else { -1 },
            right: if r < n { r } else { -1 },
        });
    }
    nodes
}

fn left_height(nodes: &[Node], idx: i64) -> i64 {
    let mut h = 0i64;
    let mut cur = idx;
    while cur != -1 {
        h += 1;
        cur = nodes[cur as usize].left;
    }
    h
}

fn right_height(nodes: &[Node], idx: i64) -> i64 {
    let mut h = 0i64;
    let mut cur = idx;
    while cur != -1 {
        h += 1;
        cur = nodes[cur as usize].right;
    }
    h
}

fn count_nodes(nodes: &[Node], idx: i64) -> i64 {
    if idx == -1 {
        return 0;
    }
    let lh = left_height(nodes, idx);
    let rh = right_height(nodes, idx);
    if lh == rh {
        return (1i64 << lh) - 1;
    }
    1 + count_nodes(nodes, nodes[idx as usize].left) + count_nodes(nodes, nodes[idx as usize].right)
}

fn main() {
    let n: i64 = 2000000;
    let passes: i64 = 2000000;
    let top_span: i64 = 2048;
    let modulus: i64 = 1000000007;

    let nodes = build(n);

    let mut sink = 0i64;
    for p in 0..passes {
        let start = p % top_span;
        sink = (sink + count_nodes(&nodes, start)) % modulus;
    }
    println!("{}", sink);
}
