//! Benchmark workload — BFS clone of a 10-regular ring of N=2000 nodes.
//!
//! Algorithmic mirror of bench/clone_bfs.kara and bench/clone_bfs.py.
//! See ../README.md § Benchmarks for the choice of N / K and the
//! ring-graph generator.
//!
//! Uses `Rc<RefCell<Node>>` to mirror Kāra's `shared struct Node`
//! semantics — reference-counted heap allocation with interior
//! mutability for the `neighbors` Vec. `black_box(&nodes[0])` keeps
//! LLVM from hoisting the pure clone_graph call out of the K outer
//! loop.

use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::hint::black_box;
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

    let nodes: Vec<NodeRef> = (0..N).map(|i| make_node((i + 1) as i64)).collect();
    for i in 0..N {
        for d in 1..=HALF_DEG {
            let j = (i + d) % N;
            nodes[i].borrow_mut().neighbors.push(Rc::clone(&nodes[j]));
            nodes[j].borrow_mut().neighbors.push(Rc::clone(&nodes[i]));
        }
    }

    let mut sum: i64 = 0;
    for _ in 0..K {
        let c = clone_graph(black_box(&nodes[0]));
        sum += c.borrow().val;
    }
    println!("{}", sum);
}
