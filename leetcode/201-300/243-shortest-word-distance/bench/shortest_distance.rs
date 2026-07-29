// Benchmark harness for LeetCode #243 — Shortest Word Distance.
// Mirrors shortest_distance.kara algorithm-for-algorithm.
//
// `.clone()` per slot is deliberate and matches the kāra mirror: each of the
// 20,000 slots owns its word, so no equality test can shortcut on the two
// operands sharing a data pointer.

fn shortest_distance(words: &[String], word1: &str, word2: &str) -> i64 {
    let n = words.len() as i64;
    let mut last1: i64 = -1;
    let mut last2: i64 = -1;
    let mut best = n;
    let mut i: i64 = 0;
    while i < n {
        if words[i as usize] == word1 {
            last1 = i;
            if last2 >= 0 {
                best = best.min(last1 - last2);
            }
        } else if words[i as usize] == word2 {
            last2 = i;
            if last1 >= 0 {
                best = best.min(last2 - last1);
            }
        }
        i += 1;
    }
    best
}

// Overflow-free 31-bit LCG; every draw uses bits 16..23.
fn lcg(state: i64) -> i64 {
    (state * 1103515245 + 12345) & 2147483647
}

fn main() {
    let vocab_n: i64 = 256;
    let n: i64 = 20000;
    let iters: i64 = 2000;

    let alpha = ["a", "b", "c", "d"];
    let mut vocab: Vec<String> = Vec::new();
    let mut v: i64 = 0;
    while v < vocab_n {
        let mut w = String::from("delta");
        w.push_str(alpha[((v / 64) % 4) as usize]);
        w.push_str(alpha[((v / 16) % 4) as usize]);
        w.push_str(alpha[((v / 4) % 4) as usize]);
        w.push_str(alpha[(v % 4) as usize]);
        vocab.push(w);
        v += 1;
    }

    let mut list: Vec<String> = Vec::new();
    let mut state: i64 = 1;
    let mut i: i64 = 0;
    while i < n {
        state = lcg(state);
        list.push(vocab[((state / 65536) % vocab_n) as usize].clone());
        i += 1;
    }

    let mut acc: i64 = 0;
    let mut qstate: i64 = 7;
    let mut k: i64 = 0;
    while k < iters {
        qstate = lcg(qstate);
        let a = (qstate / 65536) % vocab_n;
        qstate = lcg(qstate);
        let mut b = (qstate / 65536) % vocab_n;
        if b == a {
            b = (b + 1) % vocab_n;
        }
        let d = shortest_distance(&list, &vocab[a as usize], &vocab[b as usize]);
        acc = (acc * 131 + d) % 1000000007;
        k += 1;
    }
    println!("{}", acc);
}
