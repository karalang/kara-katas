// Benchmark workload — Rust mirror of simplify.kara, single-threaded.
//
// Same N=8 inputs, K=1_000_000 iters cycled by k % N. Sink is the
// sum of the simplified-output string lengths (i64). Output prints
// match the kara/c/go/py mirrors so all five impls print the same
// number before timing.

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

    let mut sum: i64 = 0;
    let mut k: i64 = 0;
    while k < k_iters {
        let idx = (k % n) as usize;
        let r = simplify(inputs[idx]);
        sum += r.len() as i64;
        k += 1;
    }
    println!("{}", sum);
}
