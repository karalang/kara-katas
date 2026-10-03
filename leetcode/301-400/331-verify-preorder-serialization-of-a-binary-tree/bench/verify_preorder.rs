// Benchmark workload for LeetCode #331 — Rust mirror of verify_preorder.kara.
// Same tree, same variants, same punches, same sink.

const NODES: i64 = 100000;
const VARIANTS: i64 = 16;
const PUNCHES: i64 = 160;
const MODULUS: i64 = 1073741789;

fn is_valid_serialization(preorder: &str) -> bool {
    let mut slots: i64 = 1;
    for tok in preorder.split(',') {
        if slots == 0 {
            return false;
        }
        if tok == "#" {
            slots -= 1;
        } else {
            slots += 1;
        }
    }
    slots == 0
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn tree(seed: &mut i64, n: i64, out: &mut Vec<String>) {
    if n == 0 {
        out.push("#".to_string());
        return;
    }
    out.push((next(seed) % 100).to_string());
    let left = next(seed) % n;
    tree(seed, left, out);
    tree(seed, n - 1 - left, out);
}

fn main() {
    let mut seed: i64 = 331;
    let mut tokens: Vec<String> = Vec::new();
    tree(&mut seed, NODES, &mut tokens);
    let mut variants: Vec<String> = Vec::new();
    for v in 0..VARIANTS {
        let kind = v % 4;
        let at = (next(&mut seed) * 32768 + next(&mut seed)) % tokens.len() as i64;
        let mut edited: Vec<String> = Vec::new();
        for (i, t) in tokens.iter().enumerate() {
            let i = i as i64;
            if i == at && kind == 1 {
                continue;
            }
            if i == at && kind == 3 {
                edited.push("#".to_string());
            }
            if i == at && kind == 2 && t == "#" {
                edited.push("7".to_string());
                edited.push("#".to_string());
            }
            edited.push(t.clone());
        }
        variants.push(edited.join(","));
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        let v = next(&mut seed) % VARIANTS;
        let answer = if is_valid_serialization(&variants[v as usize]) { 1 } else { 0 };
        sink = (sink * 1000003 + answer * 64 + v) % MODULUS;
    }
    println!("{}", sink);
}
