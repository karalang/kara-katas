// LeetCode #2296: Design a Text Editor -- the bench, the ★ arm in Rust.
// Two stacks of letters: `left` holds the text before the cursor in
// order, `right` the text after it reversed.

struct TextEditor {
    left: Vec<char>,
    right: Vec<char>,
}

impl TextEditor {
    fn new() -> Self {
        TextEditor { left: Vec::new(), right: Vec::new() }
    }

    fn add_text(&mut self, text: &str) {
        for c in text.chars() {
            self.left.push(c);
        }
    }

    fn delete_text(&mut self, k: i64) -> i64 {
        let n = k.min(self.left.len() as i64);
        for _ in 0..n {
            self.left.pop();
        }
        n
    }

    fn cursor_left(&mut self, k: i64) -> String {
        for _ in 0..k.min(self.left.len() as i64) {
            let c = self.left.pop().unwrap();
            self.right.push(c);
        }
        self.tail()
    }

    fn cursor_right(&mut self, k: i64) -> String {
        for _ in 0..k.min(self.right.len() as i64) {
            let c = self.right.pop().unwrap();
            self.left.push(c);
        }
        self.tail()
    }

    fn tail(&self) -> String {
        let from = self.left.len() - self.left.len().min(10);
        self.left[from..].iter().collect()
    }
}

fn run(calls: &[(i64, i64, String)]) -> Vec<String> {
    let mut editor = TextEditor::new();
    let mut answers = Vec::new();
    for (kind, k, text) in calls {
        match kind {
            0 => editor.add_text(text),
            1 => answers.push(format!("{}", editor.delete_text(*k))),
            2 => answers.push(editor.cursor_left(*k)),
            _ => answers.push(editor.cursor_right(*k)),
        }
    }
    answers
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn calls_of(count: usize, rng: &mut Rng) -> Vec<(i64, i64, String)> {
    let mut calls = Vec::new();
    for _ in 0..count {
        let kind = rng.next() % 4;
        let k = rng.next() % 40 + 1;
        let mut text = String::new();
        if kind == 0 {
            for _ in 0..k {
                text.push((b'a' + (rng.next() % 26) as u8) as char);
            }
        }
        calls.push((kind, k, text));
    }
    calls
}

fn main() {
    let mut rng = Rng(2296);
    let editors: Vec<Vec<(i64, i64, String)>> = (0..10).map(|_| calls_of(20000, &mut rng)).collect();
    let mut check: i64 = 0;
    for _ in 0..10 {
        for calls in &editors {
            for answer in run(calls) {
                for b in answer.bytes() {
                    check = (check * 131 + b as i64) % 1000000007;
                }
                check = (check * 131 + 1) % 1000000007;
            }
        }
    }
    println!("10 passes over 10 editors of 2 * 10^4 calls: checksum {}", check);
}
