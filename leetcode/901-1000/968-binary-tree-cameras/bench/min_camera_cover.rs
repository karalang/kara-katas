// Benchmark: LeetCode #968 Binary Tree Cameras -- the ★ arm, greedy from
// the leaves, on random trees of 1000 nodes, LeetCode's largest. Mirrors
// min_camera_cover.kara, .c, .py and go-seq/. The tree is LeetCode's Rust
// shape, `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
// `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

// 0 not yet covered, 1 holds a camera, 2 covered without one.
fn watch(t: &Tree, cameras: &mut i64) -> i64 {
    match t {
        None => 2,
        Some(node) => {
            let n = node.borrow();
            let l = watch(&n.left, cameras);
            let r = watch(&n.right, cameras);
            if l == 0 || r == 0 {
                *cameras += 1;
                1
            } else if l == 1 || r == 1 {
                2
            } else {
                0
            }
        }
    }
}

fn min_camera_cover(root: &Tree) -> i64 {
    let mut cameras = 0;
    if watch(root, &mut cameras) == 0 {
        cameras += 1;
    }
    cameras
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node() -> Node {
    Rc::new(RefCell::new(TreeNode {
        val: 0,
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
    let root = new_node();
    for _ in 1..n {
        attach(&root, new_node(), seed);
    }
    Some(root)
}

fn main() {
    let rounds = 200;
    let mut seed = 968;
    let trees: Vec<Tree> = (0..200).map(|_| random_tree(1000, &mut seed)).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..200 {
            let c = min_camera_cover(&trees[(r + i) % 200]);
            total += c;
            check = (check * 31 + c + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 200 trees of 1000 nodes: {total} cameras, checksum {check}");
}
