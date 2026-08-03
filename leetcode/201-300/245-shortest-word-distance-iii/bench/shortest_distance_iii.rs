// Benchmark mirror for LeetCode #245 - Shortest Word Distance III.
//
// Same algorithm, same LCG, same sink as the Kara/C/Go/Python mirrors, and the
// same workload as #243's bench so the two are directly comparable. Half the
// punches are same-word queries - the case #243 cannot answer.

const VOCAB_N: i64 = 256;
const N: i64 = 20000;
const ITERS: i64 = 2000;

fn shortest_word_distance(words: &[String], word1: &str, word2: &str) -> i64 {
    let n = words.len() as i64;
    let same = word1 == word2;
    let mut best = n;
    let mut prev: i64 = -1;
    for i in 0..n {
        let w = &words[i as usize];
        if w == word1 || w == word2 {
            if prev >= 0 && (same || words[prev as usize] != *w) {
                if i - prev < best {
                    best = i - prev;
                }
            }
            prev = i;
        }
    }
    best
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

    let mut acc: i64 = 0;
    let mut qstate: i64 = 7;
    for k in 0..ITERS {
        qstate = lcg(qstate);
        let a = (qstate / 65536) % VOCAB_N;
        qstate = lcg(qstate);
        let mut b = (qstate / 65536) % VOCAB_N;
        if b == a {
            b = (b + 1) % VOCAB_N;
        }
        let d = if k % 2 == 0 {
            shortest_word_distance(&list, &vocab[a as usize], &vocab[a as usize])
        } else {
            shortest_word_distance(&list, &vocab[a as usize], &vocab[b as usize])
        };
        acc = (acc * 131 + d) % 1000000007;
    }
    println!("{}", acc);
}
