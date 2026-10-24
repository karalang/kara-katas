// Benchmark: LeetCode #979 Distribute Coins in Binary Tree -- the ★ arm,
// excess from the leaves, on random trees of 100 nodes, LeetCode's
// largest. Mirrors distribute_coins.kara, .c, .py and go-seq/. The tree
// is LeetCode's Rust shape, `Option<Rc<RefCell<TreeNode>>>`, reference
// counted as Kāra's `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;
type Tree = Option<Node>;

fn excess(t: &Tree, moves: &mut i64) -> i64 {
    match t {
        None => 0,
        Some(node) => {
            let n = node.borrow();
            let l = excess(&n.left, moves);
            let r = excess(&n.right, moves);
            *moves += l.abs() + r.abs();
            n.val + l + r - 1
        }
    }
}

fn distribute_coins(root: &Tree) -> i64 {
    let mut moves = 0;
    excess(root, &mut moves);
    moves
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
    let mut nodes: Vec<Node> = vec![new_node()];
    for _ in 1..n {
        let node = new_node();
        attach(&nodes[0], node.clone(), seed);
        nodes.push(node);
    }
    for _ in 0..n {
        let k = (next_random(seed) % n as i64) as usize;
        nodes[k].borrow_mut().val += 1;
    }
    Some(nodes[0].clone())
}

fn main() {
    let rounds = 200;
    let mut seed = 979;
    let trees: Vec<Tree> = (0..2000).map(|_| random_tree(100, &mut seed)).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..2000 {
            let m = distribute_coins(&trees[(r + i) % 2000]);
            total += m;
            check = (check * 31 + m + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 2000 trees of 100 nodes: {total} moves, checksum {check}");
}
