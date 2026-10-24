// Benchmark: LeetCode #987 Vertical Order Traversal of a Binary Tree --
// the ★ arm, every node's place sorted, on random trees of 1000 nodes,
// LeetCode's largest. Mirrors vertical_traversal.kara, .c, .py and
// go-seq/. The tree is LeetCode's Rust shape,
// `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
// `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

fn walk(t: &Tree, row: i64, col: i64, out: &mut Vec<(i64, i64, i64)>) {
    if let Some(node) = t {
        let n = node.borrow();
        out.push((col, row, n.val));
        walk(&n.left, row + 1, col - 1, out);
        walk(&n.right, row + 1, col + 1, out);
    }
}

fn vertical_traversal(root: &Tree) -> Vec<Vec<i64>> {
    let mut places: Vec<(i64, i64, i64)> = Vec::new();
    walk(root, 0, 0, &mut places);
    places.sort();
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut last = 0;
    for (col, _, val) in places {
        if out.is_empty() || col != last {
            out.push(Vec::new());
            last = col;
        }
        let k = out.len() - 1;
        out[k].push(val);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(val: i64) -> Node {
    Rc::new(RefCell::new(TreeNode {
        val,
        left: None,
        right: None,
    }))
}

fn attach(root: &Node, node: Node, seed: &mut i64) {
    let mut cur = root.clone();
    loop {
        let go_left = next_random(seed) % 2 == 0;
        let next = if go_left {
            cur.borrow().left.clone()
        } else {
            cur.borrow().right.clone()
        };
        match next {
            Some(child) => cur = child,
            None => {
                if go_left {
                    cur.borrow_mut().left = Some(node);
                } else {
                    cur.borrow_mut().right = Some(node);
                }
                return;
            }
        }
    }
}

fn random_tree(n: usize, seed: &mut i64) -> Tree {
    let root = new_node(next_random(seed) % 1001);
    for _ in 1..n {
        let node = new_node(next_random(seed) % 1001);
        attach(&root, node, seed);
    }
    Some(root)
}

fn main() {
    let rounds = 500;
    let mut seed = 987;
    let trees: Vec<Tree> = (0..20).map(|_| random_tree(1000, &mut seed)).collect();
    let mut columns: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let cols = vertical_traversal(&trees[(r + i) % 20]);
            columns += cols.len() as i64;
            let mid = &cols[cols.len() / 2];
            check = (check * 31 + mid.len() as i64 + mid[0]) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 trees of 1000 nodes: {columns} columns, checksum {check}");
}
