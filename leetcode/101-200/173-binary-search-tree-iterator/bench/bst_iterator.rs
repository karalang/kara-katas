struct Node {
    val: i64,
    left: i64,
    right: i64,
}

fn insert(nodes: &mut Vec<Node>, root: i64, val: i64) -> i64 {
    if root == -1 {
        nodes.push(Node { val, left: -1, right: -1 });
        return nodes.len() as i64 - 1;
    }
    if val < nodes[root as usize].val {
        let li = nodes[root as usize].left;
        let l = insert(nodes, li, val);
        nodes[root as usize].left = l;
    } else {
        let ri = nodes[root as usize].right;
        let r = insert(nodes, ri, val);
        nodes[root as usize].right = r;
    }
    root
}

fn main() {
    let n: i64 = 4000;
    let passes: i64 = 30000;

    let mut nodes: Vec<Node> = Vec::new();
    let mut root: i64 = -1;
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = state % 1000;
        root = insert(&mut nodes, root, v);
    }

    let mut stack: Vec<i64> = Vec::new();
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 1315423911 + 7) % n) as usize;
        nodes[idx].val = (nodes[idx].val + 1) % 1000;

        stack.clear();
        let mut cur = root;
        while cur != -1 {
            stack.push(cur);
            cur = nodes[cur as usize].left;
        }
        let mut pos: i64 = 1;
        while !stack.is_empty() {
            let top = stack.pop().unwrap();
            sink += pos * nodes[top as usize].val;
            pos += 1;
            let mut r = nodes[top as usize].right;
            while r != -1 {
                stack.push(r);
                r = nodes[r as usize].left;
            }
        }
    }
    println!("{}", sink);
}
