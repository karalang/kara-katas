// LeetCode 297 benchmark lane — Rust mirror of treecodec.kara.
//
// Same algorithm, same tree shape, same sink: build one balanced 200k-node
// tree, then 24 chained serialize/deserialize round trips, hashing every
// encoded string. See the .kara file's header for the workload rationale.

struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn build(vals: &[i64], lo: usize, hi: usize) -> Option<Box<Node>> {
    if lo >= hi {
        return None;
    }
    let mid = lo + (hi - lo) / 2;
    let l = build(vals, lo, mid);
    let r = build(vals, mid + 1, hi);
    Some(Box::new(Node { val: vals[mid], left: l, right: r }))
}

fn ser_into(t: &Option<Box<Node>>, out: &mut String) {
    if !out.is_empty() {
        out.push(',');
    }
    match t {
        None => out.push('#'),
        Some(n) => {
            out.push_str(&n.val.to_string());
            ser_into(&n.left, out);
            ser_into(&n.right, out);
        }
    }
}

fn serialize(t: &Option<Box<Node>>) -> String {
    let mut out = String::new();
    ser_into(t, &mut out);
    out
}

fn de_at(toks: &[&str], i: &mut usize) -> Option<Box<Node>> {
    let tok = toks[*i];
    *i += 1;
    if tok == "#" {
        return None;
    }
    let v: i64 = tok.parse().unwrap_or(0);
    let l = de_at(toks, i);
    let r = de_at(toks, i);
    Some(Box::new(Node { val: v, left: l, right: r }))
}

fn deserialize(s: &str) -> Option<Box<Node>> {
    let toks: Vec<&str> = s.split(',').collect();
    let mut i = 0usize;
    de_at(&toks, &mut i)
}

fn hash_string(s: &str, seed: i64) -> i64 {
    let mut h = seed;
    for b in s.as_bytes() {
        h = (h * 131 + *b as i64) % 1_000_000_007;
    }
    h
}

// A 200k-node balanced tree drops through ~18 levels of `Box` on the way out,
// which is fine; the recursion in `build`/`ser_into`/`de_at` is the same depth.
fn main() {
    let n: usize = 200_000;
    let rounds = 24;

    let mut vals = Vec::with_capacity(n);
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7fff_ffff;
        vals.push(state % 1000003 - 500000);
    }

    let mut tree = build(&vals, 0, n);
    let mut checksum: i64 = 0;

    for _ in 0..rounds {
        let s = serialize(&tree);
        checksum = hash_string(&s, checksum);
        tree = deserialize(&s);
    }

    println!("nodes {} rounds {} checksum {}", n, rounds, checksum);
}
