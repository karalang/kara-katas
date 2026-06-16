// LeetCode #71 — rayon-parallel Rust mirror (par lane, simplify).
// Same one-pass simplify as ../simplify.rs; the K=1M reduction runs across a
// rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink (sum of
// simplified-output lengths) matches the kara/rust/c/go mirrors.

fn simplify(s: &str) -> String {
    let cs: Vec<char> = s.chars().collect();
    let n: i64 = cs.len() as i64;

    let mut starts: Vec<i64> = Vec::new();
    let mut ends: Vec<i64> = Vec::new();

    let mut i: i64 = 0;
    while i < n {
        while i < n && cs[i as usize] == '/' {
            i += 1;
        }
        if i >= n {
            break;
        }
        let mut j: i64 = i;
        while j < n && cs[j as usize] != '/' {
            j += 1;
        }
        let len = j - i;

        let is_dot = len == 1 && cs[i as usize] == '.';
        let is_dotdot = len == 2 && cs[i as usize] == '.' && cs[(i + 1) as usize] == '.';

        if is_dot {
        } else if is_dotdot {
            starts.pop();
            ends.pop();
        } else {
            starts.push(i);
            ends.push(j);
        }
        i = j;
    }

    if starts.is_empty() {
        return String::from("/");
    }

    let mut out = String::new();
    for k in 0..starts.len() {
        out.push('/');
        let a = starts[k] as usize;
        let b = ends[k] as usize;
        for p in a..b {
            out.push(cs[p]);
        }
    }
    out
}

fn main() {
    use rayon::prelude::*;
    let inputs: [&str; 8] = [
        "/home/",
        "/home/user/Documents/../Pictures",
        "/.../a/../b/c/../d/./",
        "/a/b/c/../..",
        "/a//b////c/d//././/..",
        "/abc_123",
        "/a/b/../c/../../d",
        "/...hidden",
    ];
    let n: i64 = inputs.len() as i64;
    let k_iters: i64 = 1_000_000;

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % n) as usize;
            simplify(inputs[idx]).len() as i64
        })
        .sum();
    println!("{}", sum);
}
