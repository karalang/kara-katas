// LeetCode #1373 bench -- Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>`: one walk up from the leaves; each subtree
// reports whether it is a search tree, its smallest and largest key, and
// its sum.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

struct Summary {
    search: bool,
    low: i64,
    high: i64,
    sum: i64,
}

fn summarize(node: &Option<Node>, best: &mut i64) -> Summary {
    let Some(n) = node else {
        // an empty tree is a search tree with no keys
        return Summary { search: true, low: i64::MAX, high: i64::MIN, sum: 0 };
    };
    let n = n.borrow();
    let l = summarize(&n.left, best);
    let r = summarize(&n.right, best);
    let key = n.val as i64;
    if l.search && r.search && l.high < key && key < r.low {
        let sum = l.sum + key + r.sum;
        *best = (*best).max(sum);
        return Summary { search: true, low: l.low.min(key), high: r.high.max(key), sum };
    }
    Summary { search: false, low: 0, high: 0, sum: 0 }
}

fn max_sum_bst(root: Option<Node>) -> i32 {
    let mut best = 0;
    summarize(&root, &mut best);
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(val: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn main() {
    // 4 search trees of 4 * 10^4 nodes, keys from -4 * 10^4 to 4 * 10^4
    // put in one by one, a key already there skipped, built once; then 300
    // rounds, each giving one node of one tree a new key, both drawn from
    // the checksum so far, and finding that tree's largest search tree
    let mut seed = 1373i64;
    let mut roots: Vec<Node> = Vec::new();
    let mut nodes: Vec<Vec<Node>> = Vec::new();
    for _ in 0..4 {
        let root = new_node(0);
        let mut all = vec![root.clone()];
        while all.len() < 40000 {
            let a = next_random(&mut seed);
            let key = ((a * 32768 + next_random(&mut seed)) % 80001 - 40000) as i32;
            let mut at = root.clone();
            loop {
                let val = at.borrow().val;
                if key == val {
                    break;
                }
                let next = if key < val { at.borrow().left.clone() } else { at.borrow().right.clone() };
                match next {
                    Some(child) => at = child,
                    None => {
                        let node = new_node(key);
                        if key < val {
                            at.borrow_mut().left = Some(node.clone());
                        } else {
                            at.borrow_mut().right = Some(node.clone());
                        }
                        all.push(node);
                        break;
                    }
                }
            }
        }
        roots.push(root);
        nodes.push(all);
    }
    let mut check: i64 = 0;
    for r in 0..300i64 {
        let t = (check % 4) as usize;
        nodes[t][((check / 4) % 40000) as usize].borrow_mut().val = ((check / 160000) % 80001 - 40000) as i32;
        let got = max_sum_bst(Some(roots[t].clone())) as i64;
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("300 rounds over 4 trees of 40000 nodes: checksum {check}");
}
