struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn insert(nodes: &mut Vec<Node>, root: i64, v: i64) -> i64 {
    if root == -1 {
        let idx = nodes.len() as i64;
        nodes.push(Node {
            val: v,
            left: -1,
            right: -1,
        });
        return idx;
    }
    if v < nodes[root as usize].val {
        let l = insert(nodes, nodes[root as usize].left, v);
        nodes[root as usize].left = l;
    } else {
        let r = insert(nodes, nodes[root as usize].right, v);
        nodes[root as usize].right = r;
    }
    root
}

fn kth_smallest(nodes: &[Node], root: i64, k: i64) -> i64 {
    let mut stack: Vec<i64> = Vec::new();
    let mut cur = root;
    let mut count = 0i64;
    while cur != -1 || !stack.is_empty() {
        while cur != -1 {
            stack.push(cur);
            cur = nodes[cur as usize].left;
        }
        let node = stack.pop().unwrap();
        count += 1;
        if count == k {
            return nodes[node as usize].val;
        }
        cur = nodes[node as usize].right;
    }
    -1
}

fn main() {
    let n: i64 = 3000;
    let queries: i64 = 140000;

    let mut nodes: Vec<Node> = Vec::new();
    let mut root: i64 = -1;
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        root = insert(&mut nodes, root, state);
    }

    let mut sink: i64 = 0;
    for _ in 0..queries {
        state = (state * 1103515245 + 12345) & 2147483647;
        let k = 1 + (state % n);
        sink += kth_smallest(&nodes, root, k);
    }
    println!("{}", sink);
}
