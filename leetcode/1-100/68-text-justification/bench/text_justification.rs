// Benchmark workload — Text Justification (LeetCode #68).
// Rust mirror of bench/text_justification.kara. The ★'s greedy-pack + even-spread
// logic streaming emitted bytes (word chars + gap spaces) into a rolling
// polynomial hash — no per-call allocation. Fixed 40-word list, justified
// K=300_000 times at a swept width. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

const WORDS: [&str; 40] = [
    "the", "quick", "brown", "fox", "jumps", "over", "a", "lazy", "dog", "while", "gentle",
    "breeze", "carries", "autumn", "leaves", "across", "quiet", "meadow", "near", "old",
    "stone", "bridge", "where", "children", "often", "gather", "to", "watch", "river", "flow",
    "beneath", "ancient", "willow", "trees", "and", "listen", "as", "the", "wind", "hums",
];
const MOD: i64 = 1_000_000_007;

fn justify_hash(max_width: i64, mut h: i64) -> i64 {
    let n = WORDS.len() as i64;
    let mut i = 0i64;
    while i < n {
        let mut j = i;
        let mut line_chars = 0i64;
        let mut count = 0i64;
        while j < n {
            let wl = WORDS[j as usize].len() as i64;
            if line_chars + wl + count <= max_width {
                line_chars += wl;
                count += 1;
                j += 1;
            } else {
                break;
            }
        }
        let gaps = count - 1;
        let total = max_width - line_chars;
        let is_last = j == n;

        if is_last || count == 1 {
            let mut used = 0i64;
            for g in 0..count {
                for b in WORDS[(i + g) as usize].bytes() {
                    h = (h * 131 + b as i64) % MOD;
                    used += 1;
                }
                if g < count - 1 {
                    h = (h * 131 + 32) % MOD;
                    used += 1;
                }
            }
            while used < max_width {
                h = (h * 131 + 32) % MOD;
                used += 1;
            }
        } else {
            let base = total / gaps;
            let extra = total % gaps;
            for g in 0..count {
                for b in WORDS[(i + g) as usize].bytes() {
                    h = (h * 131 + b as i64) % MOD;
                }
                if g < gaps {
                    let sp = base + if g < extra { 1 } else { 0 };
                    for _ in 0..sp {
                        h = (h * 131 + 32) % MOD;
                    }
                }
            }
        }
        i = j;
    }
    h
}

fn main() {
    let total: i64 = 300_000;
    let span: i64 = 40;

    let mut acc: i64 = 0;
    for k in 0..total {
        let width = 10 + (k % span);
        acc = std::hint::black_box(justify_hash(width, acc));
    }
    println!("{}", acc);
}
