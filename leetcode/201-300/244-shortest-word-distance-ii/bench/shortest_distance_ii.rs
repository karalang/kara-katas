// Benchmark mirror for LeetCode #244 - Shortest Word Distance II.
//
// Same algorithm, same LCG, same sink as the Kara/C/Go/Python mirrors: build
// the 20,000-word list and its position index ONCE (index-pool construction -
// word -> slot in a HashMap, plus a side Vec<Vec<i64>>), then punch 200,000
// two-pointer merge queries.
//
// Uses the stock `std::collections::HashMap` with its default SipHash hasher.
// That is the honest baseline: swapping in FxHash would measure a different
// map than the one a Rust program gets by default.

use std::collections::HashMap;

const VOCAB_N: i64 = 256;
const N: i64 = 20000;
const ITERS: i64 = 200000;

struct WordDistance {
    slot: HashMap<String, usize>,
    lists: Vec<Vec<i64>>,
    size: i64,
}

impl WordDistance {
    fn new(words: &[String]) -> WordDistance {
        let mut slot: HashMap<String, usize> = HashMap::new();
        let mut lists: Vec<Vec<i64>> = Vec::new();
        let size = words.len() as i64;
        for (i, w) in words.iter().enumerate() {
            match slot.get(w) {
                Some(&s) => lists[s].push(i as i64),
                None => {
                    slot.insert(w.clone(), lists.len());
                    lists.push(vec![i as i64]);
                }
            }
        }
        WordDistance { slot, lists, size }
    }

    fn shortest(&self, word1: &str, word2: &str) -> i64 {
        let s1 = match self.slot.get(word1) {
            Some(&s) => s,
            None => return self.size,
        };
        let s2 = match self.slot.get(word2) {
            Some(&s) => s,
            None => return self.size,
        };
        let p1 = &self.lists[s1];
        let p2 = &self.lists[s2];
        let mut best = self.size;
        let mut a = 0usize;
        let mut b = 0usize;
        while a < p1.len() && b < p2.len() {
            let d = (p1[a] - p2[b]).abs();
            if d < best {
                best = d;
            }
            if p1[a] < p2[b] {
                a += 1;
            } else {
                b += 1;
            }
        }
        best
    }
}

fn lcg(state: i64) -> i64 {
    (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647
}

fn main() {
    let alpha = ['a', 'b', 'c', 'd'];

    let mut vocab: Vec<String> = Vec::new();
    for v in 0..VOCAB_N {
        let mut w = String::from("delta");
        w.push(alpha[((v / 64) % 4) as usize]);
        w.push(alpha[((v / 16) % 4) as usize]);
        w.push(alpha[((v / 4) % 4) as usize]);
        w.push(alpha[(v % 4) as usize]);
        vocab.push(w);
    }

    // Each slot gets its OWN copy.
    let mut list: Vec<String> = Vec::new();
    let mut state: i64 = 1;
    for _ in 0..N {
        state = lcg(state);
        list.push(vocab[((state / 65536) % VOCAB_N) as usize].clone());
    }

    let wd = WordDistance::new(&list);

    let mut acc: i64 = 0;
    let mut qstate: i64 = 7;
    for _ in 0..ITERS {
        qstate = lcg(qstate);
        let a = (qstate / 65536) % VOCAB_N;
        qstate = lcg(qstate);
        let mut b = (qstate / 65536) % VOCAB_N;
        if b == a {
            b = (b + 1) % VOCAB_N;
        }
        let d = wd.shortest(&vocab[a as usize], &vocab[b as usize]);
        acc = (acc * 131 + d) % 1000000007;
    }
    println!("{}", acc);
}
