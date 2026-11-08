// LeetCode #1516 bench: the ★ arm (parent walks and a splice), as
// move.kara, over `Rc<RefCell<Node>>` as LeetCode's Rust trees are.
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    val: i64,
    children: Vec<Rc<RefCell<Node>>>,
}

type Link = Rc<RefCell<Node>>;

fn parent_of(node: &Link, val: i64) -> Option<Link> {
    for child in node.borrow().children.iter() {
        if child.borrow().val == val {
            return Some(node.clone());
        }
        let found = parent_of(child, val);
        if found.is_some() {
            return found;
        }
    }
    None
}

fn contains(node: &Link, val: i64) -> bool {
    if node.borrow().val == val {
        return true;
    }
    for child in node.borrow().children.iter() {
        if contains(child, val) {
            return true;
        }
    }
    false
}

fn move_sub_tree(root: Link, p: Link, q: Link) -> Link {
    let pv = p.borrow().val;
    let qv = q.borrow().val;
    for child in q.borrow().children.iter() {
        if child.borrow().val == pv {
            return root;
        }
    }
    let p_parent = parent_of(&root, pv);
    if contains(&p, qv) {
        let q_parent = parent_of(&root, qv).unwrap();
        q_parent.borrow_mut().children.retain(|c| c.borrow().val != qv);
        q.borrow_mut().children.push(p.clone());
        match p_parent {
            None => return q,
            Some(parent) => {
                let i = parent.borrow().children.iter().position(|c| c.borrow().val == pv).unwrap();
                parent.borrow_mut().children[i] = q.clone();
            }
        }
    } else {
        let parent = p_parent.unwrap();
        parent.borrow_mut().children.retain(|c| c.borrow().val != pv);
        q.borrow_mut().children.push(p.clone());
    }
    root
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn fold(node: &Link, check: &mut i64) {
    *check = mix(*check, node.borrow().val);
    for child in node.borrow().children.iter() {
        fold(child, check);
    }
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 1516i64;
    let nodes: Vec<Link> = (0..n).map(|v| Rc::new(RefCell::new(Node { val: v, children: Vec::new() }))).collect();
    for i in 1..n {
        let parent = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % i;
        nodes[parent as usize].borrow_mut().children.push(nodes[i as usize].clone());
    }
    let mut root = nodes[0].clone();
    let mut check = 0i64;
    for _ in 0..1000 {
        let p = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
        let q = (p + 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 1)) % n;
        root = move_sub_tree(root, nodes[p as usize].clone(), nodes[q as usize].clone());
        check = mix(check, root.borrow().val);
    }
    fold(&root, &mut check);
    println!("1000 moves in a tree of 100000 nodes: checksum {}", check);
}
