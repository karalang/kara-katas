// LeetCode #1367 bench -- Rust: the ★ arm over LeetCode's own
// `Option<Box<ListNode>>` and `Rc<RefCell<TreeNode>>`: every tree node
// tried as the start of the list, and from each the list matched down
// the tree, either child carrying the next value.
use std::cell::RefCell;
use std::rc::Rc;

struct ListNode {
    val: i32,
    next: Option<Box<ListNode>>,
}

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

// the list from `head` on read down from `node`
fn matches_from(head: &Option<Box<ListNode>>, node: &Option<Node>) -> bool {
    let Some(h) = head else {
        return true;
    };
    let Some(n) = node else {
        return false;
    };
    let n = n.borrow();
    h.val == n.val && (matches_from(&h.next, &n.left) || matches_from(&h.next, &n.right))
}

fn is_sub_path(head: &Option<Box<ListNode>>, root: &Option<Node>) -> bool {
    let Some(r) = root else {
        return false;
    };
    let r = r.borrow();
    matches_from(head, root) || is_sub_path(head, &r.left) || is_sub_path(head, &r.right)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(seed: &mut i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: (1 + next_random(seed) % 2) as i32, left: None, right: None }))
}

fn main() {
    // 20 trees of 2500 nodes valued 1 or 2, the constraints' most nodes,
    // each node hung on a random empty child place, built once; then 20000
    // rounds, each flipping one node's value and searching that tree for a
    // list of 8 to 15 values, all drawn from the checksum so far
    let mut seed = 1367i64;
    let mut trees: Vec<Vec<Node>> = Vec::new();
    for _ in 0..20 {
        let root = new_node(&mut seed);
        let mut nodes = vec![root.clone()];
        let mut places: Vec<(Node, bool)> = vec![(root.clone(), true), (root, false)];
        for _ in 1..2500 {
            let k = (next_random(&mut seed) % places.len() as i64) as usize;
            let (parent, left) = places.swap_remove(k);
            let node = new_node(&mut seed);
            if left {
                parent.borrow_mut().left = Some(node.clone());
            } else {
                parent.borrow_mut().right = Some(node.clone());
            }
            places.push((node.clone(), true));
            places.push((node.clone(), false));
            nodes.push(node);
        }
        trees.push(nodes);
    }
    let mut check: i64 = 0;
    let mut hits = 0;
    for r in 0..20000i64 {
        let nodes = &trees[(check % 20) as usize];
        {
            let mut flipped = nodes[((check / 20) % 2500) as usize].borrow_mut();
            flipped.val = 3 - flipped.val;
        }
        let m = 8 + check % 8;
        let bits = check / 7;
        let mut head: Option<Box<ListNode>> = None;
        for k in 0..m {
            head = Some(Box::new(ListNode { val: (1 + (bits >> k) % 2) as i32, next: head }));
        }
        let found = is_sub_path(&head, &Some(nodes[0].clone()));
        if found {
            hits += 1;
        }
        check = (check * 31 + m * 2 + if found { 1 } else { 0 } + r) % 1000000007;
    }
    println!("20000 rounds over 20 trees of 2500 nodes: {} found, checksum {}", hits, check);
}
