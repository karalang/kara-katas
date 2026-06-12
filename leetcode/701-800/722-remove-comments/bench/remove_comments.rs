// LeetCode #722 bench harness — Rust peer (rustc -O, single-thread).
//
// Byte-indexed segment-slicing — the same canonical algorithm as the Kāra
// mirror: scan each line's bytes, classify `/` `*` markers, and append each
// surviving run as one string slice (no per-char push). Sink = ITERS *
// (surviving chars per pass) = 30960000.

const REPS: usize = 60;
const ITERS: usize = 4000;

const TEMPLATE: [&str; 10] = [
    "int main() {            // entry point",
    "  int a = 1; /* inline */ int b = 2;",
    "  /* a multi-line",
    "     block comment that",
    "     spans several lines */ int c = a + b;",
    "  // a full line comment",
    "  int e = c * 3;        /* trailing block */",
    "  int d = a /* x */ + b /* y */ + c;",
    "  return d * 2;//done",
    "}",
];

fn remove_comments(source: &[String]) -> Vec<String> {
    let mut result: Vec<String> = Vec::new();
    let mut buffer = String::new();
    let mut in_block = false;
    for line in source {
        let bytes = line.as_bytes();
        let n = bytes.len();
        let mut seg_start = 0;
        let mut i = 0;
        while i < n {
            if !in_block {
                if i + 1 < n && bytes[i] == b'/' && bytes[i + 1] == b'/' {
                    buffer.push_str(&line[seg_start..i]);
                    seg_start = n;
                    break;
                } else if i + 1 < n && bytes[i] == b'/' && bytes[i + 1] == b'*' {
                    buffer.push_str(&line[seg_start..i]);
                    in_block = true;
                    i += 2;
                } else {
                    i += 1;
                }
            } else if i + 1 < n && bytes[i] == b'*' && bytes[i + 1] == b'/' {
                in_block = false;
                i += 2;
                seg_start = i;
            } else {
                i += 1;
            }
        }
        if !in_block {
            buffer.push_str(&line[seg_start..n]);
            if !buffer.is_empty() {
                result.push(std::mem::take(&mut buffer));
            }
        }
    }
    result
}

fn pass_len(source: &[String]) -> i64 {
    remove_comments(source).iter().map(|s| s.len() as i64).sum()
}

fn main() {
    let mut lines: Vec<String> = Vec::with_capacity(REPS * TEMPLATE.len());
    for _ in 0..REPS {
        for t in TEMPLATE {
            lines.push(t.to_string());
        }
    }
    let mut sum: i64 = 0;
    for _ in 0..ITERS {
        sum += pass_len(&lines);
    }
    println!("{}", sum);
}
