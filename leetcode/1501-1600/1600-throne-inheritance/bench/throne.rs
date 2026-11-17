// LeetCode #1600: Throne Inheritance
// -- the bench in Rust, mirroring throne.kara: each person's children in
// a HashMap<String, Vec<String>>, the dead in a HashSet<String>, the
// preorder walked with a stack of &str, through 10 reigns of 50000 calls,
// drawn first.

use std::collections::{HashMap, HashSet};

struct ThroneInheritance {
    king: String,
    children: HashMap<String, Vec<String>>,
    dead: HashSet<String>,
}

impl ThroneInheritance {
    fn new(king_name: String) -> Self {
        ThroneInheritance { king: king_name, children: HashMap::new(), dead: HashSet::new() }
    }

    fn birth(&mut self, parent_name: String, child_name: String) {
        self.children.entry(parent_name).or_default().push(child_name);
    }

    fn death(&mut self, name: String) {
        self.dead.insert(name);
    }

    fn get_inheritance_order(&self) -> Vec<String> {
        let mut order = Vec::new();
        let mut stack: Vec<&str> = vec![self.king.as_str()];
        while let Some(name) = stack.pop() {
            if !self.dead.contains(name) {
                order.push(name.to_string());
            }
            if let Some(kids) = self.children.get(name) {
                for kid in kids.iter().rev() {
                    stack.push(kid.as_str());
                }
            }
        }
        order
    }
}

enum Op {
    Birth(String, String),
    Death(String),
    Ask,
}

fn main() {
    let mut seed: i64 = 1600;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut reigns: Vec<Vec<Op>> = Vec::new();
    for _ in 0..10 {
        let mut alive: Vec<String> = vec!["king".to_string()];
        let mut born = 0;
        let mut ops: Vec<Op> = Vec::new();
        for _ in 0..50000 {
            let r = next_random() % 1000;
            if r < 500 && !alive.is_empty() {
                let parent = alive[(next_random() % alive.len() as i64) as usize].clone();
                born += 1;
                let child = format!("p{}", born);
                ops.push(Op::Birth(parent, child.clone()));
                alive.push(child);
            } else if r < 625 && !alive.is_empty() {
                let at = (next_random() % alive.len() as i64) as usize;
                ops.push(Op::Death(alive.swap_remove(at)));
            } else if r < 626 {
                ops.push(Op::Ask);
            }
        }
        reigns.push(ops);
    }
    let mut check: i64 = 0;
    let mut names: i64 = 0;
    for ops in &reigns {
        let mut throne = ThroneInheritance::new("king".to_string());
        for op in ops {
            match op {
                Op::Birth(parent, child) => throne.birth(parent.clone(), child.clone()),
                Op::Death(name) => throne.death(name.clone()),
                Op::Ask => {
                    let order = throne.get_inheritance_order();
                    names += order.len() as i64;
                    for name in &order {
                        check = (check * 31 + name.len() as i64 + 1) % 1000000007;
                    }
                }
            }
        }
    }
    println!("10 reigns of 50000 calls: {} names in the orders, checksum {}", names, check);
}
