// LeetCode #1038: Binary Search Tree to Greater Sum Tree -- bench
// Mirrors ../gst.kara; see ../README.md § Benchmarks. The tree is
// `Rc<RefCell<TreeNode>>`, the closest match to a `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn add_greater(node: &Node, above: i64) -> i64 {
    match node {
        None => above,
        Some(n) => {
            let mut n = n.borrow_mut();
            let total = add_greater(&n.right, above) + n.val;
            n.val = total;
            add_greater(&n.left, total)
        }
    }
}

fn bst_to_gst(root: &Node) -> &Node {
    add_greater(root, 0);
    root
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

// A search tree of the keys, inserted in the order given; every node is
// also listed in `nodes`, in the same order.
fn build(keys: &[i64], nodes: &mut Vec<Rc<RefCell<TreeNode>>>) -> Node {
    let root = leaf(keys[0]);
    nodes.push(root.clone());
    for &v in &keys[1..] {
        let fresh = leaf(v);
        nodes.push(fresh.clone());
        let mut node = root.clone();
        loop {
            let go_left = v < node.borrow().val;
            let next = if go_left { node.borrow().left.clone() } else { node.borrow().right.clone() };
            match next {
                Some(child) => node = child,
                None => {
                    if go_left {
                        node.borrow_mut().left = Some(fresh);
                    } else {
                        node.borrow_mut().right = Some(fresh);
                    }
                    break;
                }
            }
        }
    }
    Some(root)
}

fn main() {
    let trees = 10000;
    let rounds = 50;
    let mut seed: i64 = 1038;
    let mut pool: Vec<i64> = (0..101).collect();
    let mut roots: Vec<Node> = Vec::new();
    let mut lists: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    let mut originals: Vec<Vec<i64>> = Vec::new();
    for _ in 0..trees {
        for i in 0..100usize {
            let j = i + (next_random(&mut seed) % (101 - i as i64)) as usize;
            pool.swap(i, j);
        }
        let keys = pool[0..100].to_vec();
        let mut nodes = Vec::new();
        roots.push(build(&keys, &mut nodes));
        lists.push(nodes);
        originals.push(keys);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for t in 0..trees {
            for (node, &k) in lists[t].iter().zip(originals[t].iter()) {
                node.borrow_mut().val = k;
            }
            let top = bst_to_gst(&roots[t]).as_ref().unwrap().borrow().val;
            total += top;
            check = (check * 31 + top + 1000) % 1000000007;
        }
    }
    println!("{trees} trees of 100 keys, {rounds} rounds: total {total}, checksum {check}");
}
