// Benchmark kernel for LeetCode #341 (Flatten Nested List Iterator).
// Mirrors flatten_iterator.kara: a stack of members, with has_next()
// expanding lists until an integer is on top. 80 rounds, each building a
// pseudo-random nested list of 20,000 top-level members and draining it;
// the sink is a rolling hash of every integer in order.

enum Nested {
    Int(i64),
    List(Vec<Nested>),
}

struct NestedIterator {
    stack: Vec<Nested>,
}

impl NestedIterator {
    fn new(items: Vec<Nested>) -> NestedIterator {
        let mut it = NestedIterator { stack: Vec::new() };
        it.push_reversed(items);
        it
    }

    fn push_reversed(&mut self, mut items: Vec<Nested>) {
        while let Some(x) = items.pop() {
            self.stack.push(x);
        }
    }

    fn has_next(&mut self) -> bool {
        while let Some(top) = self.stack.pop() {
            match top {
                Nested::Int(v) => {
                    self.stack.push(Nested::Int(v));
                    return true;
                }
                Nested::List(inner) => self.push_reversed(inner),
            }
        }
        false
    }

    fn next(&mut self) -> i64 {
        self.has_next();
        match self.stack.pop() {
            Some(Nested::Int(v)) => v,
            _ => panic!("next() past the end"),
        }
    }
}

fn next_rand(state: &mut i64) -> i64 {
    *state = (*state * 1103515245 + 12345) % 2147483648;
    *state >> 8
}

fn gen_member(state: &mut i64, depth: i64, max_depth: i64) -> Nested {
    if depth < max_depth && next_rand(state) % 3 == 0 {
        let count = next_rand(state) % 5;
        let mut items = Vec::new();
        for _ in 0..count {
            items.push(gen_member(state, depth + 1, max_depth));
        }
        return Nested::List(items);
    }
    Nested::Int(next_rand(state) % 201 - 100)
}

fn gen_list(seed: i64, top: i64, max_depth: i64) -> Vec<Nested> {
    let mut state = seed;
    let mut items = Vec::new();
    for _ in 0..top {
        items.push(gen_member(&mut state, 1, max_depth));
    }
    items
}

fn main() {
    let mut h: i64 = 7;
    for r in 0..80 {
        let mut it = NestedIterator::new(gen_list(r * 7 + 1, 20000, 12));
        while it.has_next() {
            h = (h * 31 + it.next() + 101) % 1000000007;
        }
    }
    println!("{}", h);
}
