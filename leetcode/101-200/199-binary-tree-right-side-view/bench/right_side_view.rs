struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn right_view(nodes: &[Node], root: i64) -> Vec<i64> {
    let mut result: Vec<i64> = Vec::new();
    if root == -1 {
        return result;
    }
    let mut level: Vec<i64> = Vec::new();
    level.push(root);
    while !level.is_empty() {
        result.push(nodes[level[level.len() - 1] as usize].val);
        let mut next: Vec<i64> = Vec::new();
        for &idx in &level {
            if nodes[idx as usize].left != -1 {
                next.push(nodes[idx as usize].left);
            }
            if nodes[idx as usize].right != -1 {
                next.push(nodes[idx as usize].right);
            }
        }
        level = next;
    }
    result
}

fn main() {
    let n: i64 = 8191;
    let passes: i64 = 40000;

    let mut nodes: Vec<Node> = Vec::with_capacity(n as usize);
    let mut state: i64 = 12345;
    for i in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = (state >> 16) % 1000;
        let li = 2 * i + 1;
        let ri = 2 * i + 2;
        nodes.push(Node {
            val: v,
            left: if li < n { li } else { -1 },
            right: if ri < n { ri } else { -1 },
        });
    }

    let mut sink: i64 = 0;
    for _ in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % n) as usize;
        nodes[idx].val = (state >> 16) % 1000;
        let view = right_view(&nodes, 0);
        for v in &view {
            sink += *v;
        }
    }
    println!("{}", sink);
}
