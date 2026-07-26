// Equal-hash sibling of word_ladder_ii.rs — see ../README.md § Benchmarks.
//
// Identical algorithm; the only change is the HashMap hasher. Kara's
// Map[String, _] hashes with FxHash (per byte: h = h.rotate_left(5) ^ byte;
// h = h.wrapping_mul(0x517c_c1b7_2722_0a95)), the same rustc-hash construction
// used here. Rust's DEFAULT hasher is SipHash-1-3, which is DoS-resistant and
// costs more per lookup — a difference in threat model, not compiler quality.
//
// README-only lane: scripts/bench-graph.py knows four language names, so an
// extra lane would be silently dropped from the feed.

use std::collections::HashMap;
use std::hash::{BuildHasherDefault, Hasher};

const FX_SEED: u64 = 0x517c_c1b7_2722_0a95;

#[derive(Default)]
struct FxLike(u64);

impl Hasher for FxLike {
    fn write(&mut self, bytes: &[u8]) {
        let mut h = self.0;
        for &b in bytes {
            h = (h.rotate_left(5) ^ (b as u64)).wrapping_mul(FX_SEED);
        }
        self.0 = h;
    }
    fn finish(&self) -> u64 {
        self.0
    }
}

type FxMapI = HashMap<String, i64, BuildHasherDefault<FxLike>>;
type FxMapV = HashMap<String, Vec<String>, BuildHasherDefault<FxLike>>;


const MOD: i64 = 1000000007;

fn nth_letter(n: i64) -> char {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let target = n % 26;
    let mut i = 0i64;
    for ch in alphabet.chars() {
        if i == target {
            return ch;
        }
        i += 1;
    }
    'a'
}

fn replace_char(word: &str, pos: i64, new_ch: char) -> String {
    let mut out = String::new();
    let mut i = 0i64;
    for ch in word.chars() {
        if i == pos {
            out.push(new_ch);
        } else {
            out.push(ch);
        }
        i += 1;
    }
    out
}

fn neighbors(word: &str, word_set: &FxMapI) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let bytes = word.as_bytes();
    let n = bytes.len() as i64;
    let mut i = 0i64;
    while i < n {
        let orig = bytes[i as usize];
        let mut c = 0i64;
        while c < 26 {
            let ch = nth_letter(c);
            if (c + 97) != (orig as i64) {
                let cand = replace_char(word, i, ch);
                if word_set.contains_key(&cand) {
                    out.push(cand);
                }
            }
            c += 1;
        }
        i += 1;
    }
    out
}

fn path_digest(path: &Vec<String>) -> i64 {
    let mut h: i64 = 0;
    let mut idx = path.len() as i64 - 1;
    while idx >= 0 {
        let w = &path[idx as usize];
        for b in w.as_bytes() {
            h = (h * 131 + ((*b as i64) - 96)) % MOD;
        }
        h = (h * 131 + 27) % MOD;
        idx -= 1;
    }
    h
}

fn dfs(
    word: &str,
    begin: &str,
    preds: &FxMapV,
    path: &mut Vec<String>,
    count: &mut i64,
    digest: &mut i64,
) {
    if word == begin {
        *digest = (*digest + path_digest(path)) % MOD;
        *count += 1;
        return;
    }
    if let Some(plist) = preds.get(word) {
        let plist = plist.clone();
        let mut i = 0usize;
        while i < plist.len() {
            let p = plist[i].clone();
            path.push(p.clone());
            dfs(&p, begin, preds, path, count, digest);
            path.pop();
            i += 1;
        }
    }
}

struct LadderResult {
    count: i64,
    len: i64,
    digest: i64,
}

fn find_ladders(begin: String, end: String, words: &Vec<String>) -> LadderResult {
    let mut word_set: FxMapI = FxMapI::default();
    let mut wi = 0usize;
    while wi < words.len() {
        word_set.insert(words[wi].clone(), 1);
        wi += 1;
    }
    if !word_set.contains_key(&end) {
        return LadderResult { count: 0, len: 0, digest: 0 };
    }

    let mut preds: FxMapV = FxMapV::default();
    let mut visited: FxMapI = FxMapI::default();
    visited.insert(begin.clone(), 1);
    let mut cur: Vec<String> = Vec::new();
    cur.push(begin.clone());
    let mut found = false;
    let mut depth = 1i64;

    while !cur.is_empty() && !found {
        let mut in_next: FxMapI = FxMapI::default();
        let mut nxt: Vec<String> = Vec::new();
        let mut i = 0usize;
        while i < cur.len() {
            let word = cur[i].clone();
            let nbs = neighbors(&word, &word_set);
            let mut j = 0usize;
            while j < nbs.len() {
                let nb = nbs[j].clone();
                if !visited.contains_key(&nb) {
                    let mut plist: Vec<String> = match preds.get(&nb) {
                        Some(v) => v.clone(),
                        None => Vec::new(),
                    };
                    plist.push(word.clone());
                    preds.insert(nb.clone(), plist);
                    if !in_next.contains_key(&nb) {
                        if nb == end {
                            found = true;
                        }
                        in_next.insert(nb.clone(), 1);
                        nxt.push(nb);
                    }
                }
                j += 1;
            }
            i += 1;
        }
        let mut k = 0usize;
        while k < nxt.len() {
            visited.insert(nxt[k].clone(), 1);
            k += 1;
        }
        cur = nxt;
        depth += 1;
    }

    if !found {
        return LadderResult { count: 0, len: 0, digest: 0 };
    }

    let mut path: Vec<String> = Vec::new();
    path.push(end.clone());
    let mut count = 0i64;
    let mut digest = 0i64;
    dfs(&end, &begin, &preds, &mut path, &mut count, &mut digest);

    LadderResult { count, len: depth, digest }
}

fn main() {
    let alpha: i64 = 5;
    let wlen: i64 = 5;
    let iters: i64 = 24;
    let total: i64 = 3125;

    let mut words: Vec<String> = Vec::new();
    let mut idx = 0i64;
    while idx < total {
        let mut w = String::new();
        let mut d = 0i64;
        let mut rem = idx;
        let mut div = 625i64;
        while d < wlen {
            let digit = rem / div;
            w.push(nth_letter(digit));
            rem -= digit * div;
            div /= alpha;
            d += 1;
        }
        words.push(w);
        idx += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let b = ((it * 257) % total) as usize;
        let e = ((it * 613 + 1234) % total) as usize;
        let r = find_ladders(words[b].clone(), words[e].clone(), &words);
        sink = (sink * 1000003 + r.count * 7 + r.len * 13 + r.digest) % MOD;
        it += 1;
    }
    println!("{}", sink);
}
