// Benchmark for #588: Rust mirror of the ★ arm (a tree of shared nodes);
// see file_system.kara. Each node is an `Rc<RefCell<Node>>`, as a Kāra
// `shared struct` is a counted handle, and a directory keeps its
// entries in a `BTreeMap`, as the Kāra arm keeps them in a `SortedMap`.

use std::cell::RefCell;
use std::collections::BTreeMap;
use std::rc::Rc;

struct Node {
    is_file: bool,
    content: String,
    children: BTreeMap<String, Rc<RefCell<Node>>>,
}

fn new_node() -> Rc<RefCell<Node>> {
    Rc::new(RefCell::new(Node { is_file: false, content: String::new(), children: BTreeMap::new() }))
}

struct FileSystem {
    root: Rc<RefCell<Node>>,
}

impl FileSystem {
    fn new() -> FileSystem {
        FileSystem { root: new_node() }
    }

    fn walk(&self, path: &str, make: bool) -> Rc<RefCell<Node>> {
        let mut node = self.root.clone();
        for name in path.split('/') {
            if name.is_empty() {
                continue;
            }
            if make && !node.borrow().children.contains_key(name) {
                node.borrow_mut().children.insert(name.to_string(), new_node());
            }
            let next = node.borrow().children[name].clone();
            node = next;
        }
        node
    }

    fn ls(&self, path: &str) -> Vec<String> {
        let node = self.walk(path, false);
        let node = node.borrow();
        if node.is_file {
            return vec![path.split('/').last().unwrap().to_string()];
        }
        let mut names: Vec<String> = Vec::new();
        for name in node.children.keys() {
            names.push(name.clone());
        }
        names
    }

    fn mkdir(&mut self, path: &str) {
        self.walk(path, true);
    }

    fn add_content_to_file(&mut self, file_path: &str, content: &str) {
        let node = self.walk(file_path, true);
        let mut node = node.borrow_mut();
        node.is_file = true;
        node.content.push_str(content);
    }

    fn read_content_from_file(&self, file_path: &str) -> String {
        self.walk(file_path, false).borrow().content.clone()
    }
}

// ---- benchmark --------------------------------------------------------------

enum Op {
    Ls(String),
    Mkdir(String),
    Add(String, String),
    Read(String),
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn dir_path(depth: i64, seed: &mut i64) -> String {
    let alphabet = "abcde";
    let mut path = String::new();
    for _ in 0..depth {
        let k = (next_random(seed) % 5) as usize;
        path.push_str("/");
        path.push_str(&alphabet[k..k + 1]);
    }
    path
}

fn script(seed: &mut i64) -> Vec<Op> {
    let names = "fghij";
    let mut made: Vec<String> = vec!["/".to_string()];
    let mut files: Vec<String> = Vec::new();
    let mut ops: Vec<Op> = Vec::new();
    while ops.len() < 300 {
        let roll = next_random(seed) % 10;
        if roll < 3 {
            let i = (next_random(seed) % made.len() as i64) as usize;
            ops.push(Op::Ls(made[i].clone()));
        } else if roll < 4 && !files.is_empty() {
            let i = (next_random(seed) % files.len() as i64) as usize;
            ops.push(Op::Read(files[i].clone()));
        } else if roll < 7 {
            let depth = 1 + next_random(seed) % 4;
            let path = dir_path(depth, seed);
            made.push(path.clone());
            ops.push(Op::Mkdir(path));
        } else {
            let k = (next_random(seed) % 5) as usize;
            let depth = next_random(seed) % 4;
            let path = format!("{}/{}", dir_path(depth, seed), &names[k..k + 1]);
            let mut content = String::new();
            for _ in 0..1 + next_random(seed) % 5 {
                let c = (next_random(seed) % 5) as usize;
                content.push_str(&names[c..c + 1]);
            }
            made.push(path.clone());
            files.push(path.clone());
            ops.push(Op::Add(path, content));
        }
    }
    ops
}

fn main() {
    let count: i64 = 200;
    let rounds: i64 = 200;
    let mut seed: i64 = 588;
    let mut scripts: Vec<Vec<Op>> = Vec::new();
    for _ in 0..count {
        scripts.push(script(&mut seed));
    }
    let mut lines: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let ops = &scripts[((round * 7 + g) % count) as usize];
            let mut fs = FileSystem::new();
            for op in ops.iter() {
                match op {
                    Op::Ls(path) => {
                        for name in fs.ls(path).iter() {
                            checksum = (checksum * 31 + name.len() as i64) % 1000000007;
                        }
                        lines += 1;
                    }
                    Op::Mkdir(path) => fs.mkdir(path),
                    Op::Add(path, content) => fs.add_content_to_file(path, content),
                    Op::Read(path) => {
                        checksum = (checksum * 31 + fs.read_content_from_file(path).len() as i64) % 1000000007;
                        lines += 1;
                    }
                }
            }
        }
    }
    println!("{} scripts of 300 commands, {} rounds: {} answers, checksum {}", count, rounds, lines, checksum);
}
