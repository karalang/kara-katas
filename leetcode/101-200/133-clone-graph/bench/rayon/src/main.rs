// LeetCode #133 — rayon-parallel Rust mirror (par lane, clone_bfs).
// Same BFS clone of a 10-regular ring (N=2000) as ../clone_bfs.rs; the K=500
// clone reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par. Sink = 500 (K × root clone val 1).
//
// `Rc<RefCell<Node>>` (mirroring Kāra's `shared struct`) is not `Send`, so the
// input graph cannot be shared across rayon worker threads. Each worker builds
// its OWN thread-local graph once, then runs its chunk of clones — the per-clone
// work is identical to the seq lane; only the cheap O(N·deg) build is duplicated
// per worker (~18×, negligible vs 500 clones). clone_graph allocates, so it is
// not hoisted (the seq lane uses black_box defensively; not needed here).
use rayon::prelude::*;
use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::rc::Rc;

type NodeRef = Rc<RefCell<Node>>;

struct Node {
    val: i64,
    neighbors: Vec<NodeRef>,
}

fn make_node(val: i64) -> NodeRef {
    Rc::new(RefCell::new(Node {
        val,
        neighbors: Vec::new(),
    }))
}

fn build_graph(n: usize, half_deg: usize) -> Vec<NodeRef> {
    let nodes: Vec<NodeRef> = (0..n).map(|i| make_node((i + 1) as i64)).collect();
    for i in 0..n {
        for d in 1..=half_deg {
            let j = (i + d) % n;
            nodes[i].borrow_mut().neighbors.push(Rc::clone(&nodes[j]));
            nodes[j].borrow_mut().neighbors.push(Rc::clone(&nodes[i]));
        }
    }
    nodes
}

fn clone_graph(root: &NodeRef) -> NodeRef {
    let root_val = root.borrow().val;
    let mut visited: HashMap<i64, NodeRef> = HashMap::new();
    visited.insert(root_val, make_node(root_val));
    let mut queue: VecDeque<NodeRef> = VecDeque::new();
    queue.push_back(Rc::clone(root));

    while let Some(curr) = queue.pop_front() {
        let curr_val = curr.borrow().val;
        let curr_clone = Rc::clone(&visited[&curr_val]);
        let curr_b = curr.borrow();
        for nb in &curr_b.neighbors {
            let nb_val = nb.borrow().val;
            if !visited.contains_key(&nb_val) {
                visited.insert(nb_val, make_node(nb_val));
                queue.push_back(Rc::clone(nb));
            }
            curr_clone
                .borrow_mut()
                .neighbors
                .push(Rc::clone(&visited[&nb_val]));
        }
    }

    Rc::clone(&visited[&root_val])
}

fn main() {
    const N: usize = 2000;
    const HALF_DEG: usize = 5;
    const K: usize = 500;
    let workers = rayon::current_num_threads().min(K);
    let chunk = K / workers;

    let sum: i64 = (0..workers)
        .into_par_iter()
        .map(|w| {
            let nodes = build_graph(N, HALF_DEG); // thread-local Rc graph
            let start = w * chunk;
            let end = if w == workers - 1 { K } else { start + chunk };
            let mut s: i64 = 0;
            for _ in start..end {
                s += clone_graph(&nodes[0]).borrow().val;
            }
            s
        })
        .sum();
    println!("{}", sum);
}
