// Benchmark for #642: mirror of autocomplete.kara (the ★ arm: a trie
// searched below the prefix) on the same workload.

struct Node {
    children: Vec<i64>,
    count: i64,
}

struct AutocompleteSystem {
    nodes: Vec<Node>,
    typed: String,
    at: i64,
}

fn branch(c: char) -> i64 {
    if c == ' ' { 26 } else { c as i64 - 'a' as i64 }
}

fn letter(b: i64) -> char {
    if b == 26 { ' ' } else { ('a' as i64 + b) as u8 as char }
}

fn new_node() -> Node {
    Node { children: vec![-1; 27], count: 0 }
}

fn gather(nodes: &Vec<Node>, node: i64, path: &String, found: &mut Vec<(i64, String)>) {
    let n = &nodes[node as usize];
    if n.count > 0 {
        found.push((n.count, path.clone()));
    }
    for b in 0..27 {
        let child = n.children[b as usize];
        if child != -1 {
            gather(nodes, child, &format!("{}{}", path, letter(b)), found);
        }
    }
}

impl AutocompleteSystem {
    fn new(sentences: &Vec<String>, times: &Vec<i64>) -> AutocompleteSystem {
        let mut system = AutocompleteSystem { nodes: vec![new_node()], typed: String::new(), at: 0 };
        for i in 0..sentences.len() {
            system.add(&sentences[i], times[i]);
        }
        system
    }

    fn add(&mut self, sentence: &String, times: i64) {
        let mut node = 0usize;
        for c in sentence.chars() {
            let b = branch(c) as usize;
            if self.nodes[node].children[b] == -1 {
                self.nodes.push(new_node());
                let last = self.nodes.len() as i64 - 1;
                self.nodes[node].children[b] = last;
            }
            node = self.nodes[node].children[b] as usize;
        }
        self.nodes[node].count += times;
    }

    fn input(&mut self, c: char) -> Vec<String> {
        if c == '#' {
            let sentence = self.typed.clone();
            self.add(&sentence, 1);
            self.typed = String::new();
            self.at = 0;
            return Vec::new();
        }
        self.typed.push(c);
        if self.at != -1 {
            self.at = self.nodes[self.at as usize].children[branch(c) as usize];
        }
        let mut top = Vec::new();
        if self.at == -1 {
            return top;
        }
        let mut found: Vec<(i64, String)> = Vec::new();
        gather(&self.nodes, self.at, &self.typed, &mut found);
        found.sort_by(|a, b| if a.0 != b.0 { b.0.cmp(&a.0) } else { a.1.cmp(&b.1) });
        for i in 0..found.len() {
            if i == 3 {
                break;
            }
            top.push(found[i].1.clone());
        }
        top
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_sentence(most: i64, seed: &mut i64) -> String {
    let length = 1 + next_random(seed) % most;
    let mut s = String::new();
    for _ in 0..length {
        let r = next_random(seed) % 4;
        s.push(if r == 0 { 'a' } else if r == 1 { 'b' } else if r == 2 { 'c' } else { ' ' });
    }
    s
}

fn main() {
    let mut seed: i64 = 642;
    let mut histories: Vec<(Vec<String>, Vec<i64>, String)> = Vec::new();
    for _ in 0..10 {
        let mut sentences: Vec<String> = Vec::new();
        let mut times: Vec<i64> = Vec::new();
        while sentences.len() < 100 {
            let s = random_sentence(100, &mut seed);
            if !sentences.contains(&s) {
                sentences.push(s);
                times.push(1 + next_random(&mut seed) % 100);
            }
        }
        let mut typing = String::new();
        while typing.len() < 5000 {
            if next_random(&mut seed) % 2 == 0 {
                let i = (next_random(&mut seed) % 100) as usize;
                typing.push_str(&sentences[i]);
            } else {
                typing.push_str(&random_sentence(100, &mut seed));
            }
            typing.push('#');
        }
        typing.truncate(5000);
        histories.push((sentences, times, typing));
    }
    let rounds = 40;
    let mut names: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let h = &histories[r % 10];
        let mut system = AutocompleteSystem::new(&h.0, &h.1);
        for c in h.2.chars() {
            let got = system.input(c);
            for name in got.iter() {
                let bytes = name.as_bytes();
                checksum = (checksum * 31
                    + name.len() as i64 * 65536
                    + bytes[0] as i64 * 256
                    + bytes[name.len() - 1] as i64)
                    % 1000000007;
                names += 1;
            }
            checksum = (checksum * 31 + 1) % 1000000007;
        }
    }
    println!("{} rounds of 5000 calls: {} names, checksum {}", rounds, names, checksum);
}
