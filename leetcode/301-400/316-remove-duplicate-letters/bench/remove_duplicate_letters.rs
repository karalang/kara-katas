// Benchmark lane for LeetCode 316 — Rust mirror of bench/remove_duplicate_letters.kara.
// Generate N drifting letters once, then PASSES monotone-stack passes (record
// each letter's last occurrence, then skip placed letters and pop larger tops
// that still have a later copy), each after overwriting one position chosen
// from the checksum.

const N: i64 = 4000000;
const PASSES: i64 = 100;
const MASK: i64 = 1073741823;

fn lcg(s: i64) -> i64 {
    (s * 1103515245 + 12345) & 0x7fffffff
}

fn remove_duplicate_letters(bs: &[u8]) -> Vec<u8> {
    let n = bs.len();
    let mut last = [-1i64; 26];
    for i in 0..n {
        last[(bs[i] - b'a') as usize] = i as i64;
    }
    let mut on_stack = [false; 26];
    let mut stack: Vec<u8> = Vec::new();
    for i in 0..n {
        let c = bs[i];
        let ci = (c - b'a') as usize;
        if on_stack[ci] {
            continue;
        }
        while let Some(&top) = stack.last() {
            if top > c && last[(top - b'a') as usize] > i as i64 {
                stack.pop();
                on_stack[(top - b'a') as usize] = false;
            } else {
                break;
            }
        }
        stack.push(c);
        on_stack[ci] = true;
    }
    stack
}

fn main() {
    let mut seed: i64 = 316;
    let mut text: Vec<u8> = Vec::with_capacity(N as usize);
    let mut cur: i64 = 25;
    for _ in 0..N {
        seed = lcg(seed);
        let r = seed / 65536;
        if r % 4 != 0 {
            cur -= 1;
            if cur < 0 {
                cur = 25;
            }
        } else {
            cur = r % 26;
        }
        text.push(cur as u8 + b'a');
    }

    let mut checksum: i64 = 0;
    for _ in 0..PASSES {
        let i = (checksum % N) as usize;
        let letter = ((checksum * 7 + 13) % 26) as u8;
        let saved = text[i];
        text[i] = letter + b'a';
        let out = remove_duplicate_letters(&text);
        let mut fold: i64 = 0;
        for &b in &out {
            fold = (fold * 131 + b as i64) & MASK;
        }
        checksum = (checksum * 31 + fold + out.len() as i64) & MASK;
        text[i] = saved;
    }
    println!("checksum {}", checksum);
}
