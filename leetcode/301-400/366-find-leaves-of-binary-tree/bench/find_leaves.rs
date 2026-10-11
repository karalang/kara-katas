// Benchmark for #366 -- mirror of find_leaves.kara. The shared enum is an
// Rc-counted enum here.
use std::collections::VecDeque;
use std::rc::Rc;

enum Tree {
    Empty,
    Node(i64, Rc<Tree>, Rc<Tree>),
}

struct Links {
    vals: Vec<i64>,
    left: Vec<i64>,
    right: Vec<i64>,
}

fn links(items: &[Option<i64>]) -> Links {
    let mut l = Links { vals: Vec::new(), left: Vec::new(), right: Vec::new() };
    match items.first() {
        Some(Some(v)) => {
            l.vals.push(*v);
            l.left.push(-1);
            l.right.push(-1);
        }
        _ => return l,
    }
    let mut queue = VecDeque::new();
    queue.push_back(0usize);
    let mut i = 1;
    while i < items.len() {
        let parent = match queue.pop_front() {
            Some(p) => p,
            None => break,
        };
        for side in 0..2 {
            if i < items.len() {
                if let Some(v) = items[i] {
                    let id = l.vals.len();
                    l.vals.push(v);
                    l.left.push(-1);
                    l.right.push(-1);
                    if side == 0 {
                        l.left[parent] = id as i64;
                    } else {
                        l.right[parent] = id as i64;
                    }
                    queue.push_back(id);
                }
                i += 1;
            }
        }
    }
    l
}

fn build(l: &Links, id: i64) -> Rc<Tree> {
    if id < 0 {
        Rc::new(Tree::Empty)
    } else {
        let i = id as usize;
        Rc::new(Tree::Node(l.vals[i], build(l, l.left[i]), build(l, l.right[i])))
    }
}

fn file_by_height(t: &Tree, out: &mut Vec<Vec<i64>>) -> i64 {
    match t {
        Tree::Empty => -1,
        Tree::Node(v, left, right) => {
            let h = 1 + file_by_height(left, out).max(file_by_height(right, out));
            if h as usize == out.len() {
                out.push(Vec::new());
            }
            out[h as usize].push(*v);
            h
        }
    }
}

fn find_leaves(items: &[Option<i64>]) -> Vec<Vec<i64>> {
    let l = links(items);
    let mut out = Vec::new();
    if !l.vals.is_empty() {
        file_by_height(&build(&l, 0), &mut out);
    }
    out
}

fn main() {
    let mut seed: i64 = 366;
    let mut checksum: i64 = 0;
    let mut groups = 0;
    for _ in 0..5 {
        let mut items = Vec::new();
        for k in 0..400000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let r = seed / 65536;
            items.push(if k > 0 && r % 4 == 0 { None } else { Some(r % 201 - 100) });
        }
        for group in find_leaves(&items) {
            groups += 1;
            for v in group {
                checksum = (checksum * 31 + v + 101) % 1000000007;
            }
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    println!("{groups} groups, checksum {checksum}");
}
