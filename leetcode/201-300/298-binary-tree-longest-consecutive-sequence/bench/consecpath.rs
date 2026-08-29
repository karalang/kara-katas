// LeetCode 298 benchmark lane — Rust mirror of consecpath.kara.
//
// Same tree, same passes, same sink: build one perfect depth-20 tree, then 40
// full traversals with steps 1..40. See the .kara file's header for the
// workload rationale.

struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn build(depth: i32, parent_val: i64, state: &mut i64) -> Option<Box<Node>> {
    if depth <= 0 {
        return None;
    }
    *state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7fff_ffff;
    let v = parent_val + *state % 3 - 1;
    let l = build(depth - 1, v, state);
    let r = build(depth - 1, v, state);
    Some(Box::new(Node { val: v, left: l, right: r }))
}

fn down(t: &Option<Box<Node>>, step: i64, best: &mut i64) -> i64 {
    let n = match t {
        None => return 0,
        Some(n) => n,
    };
    let l = down(&n.left, step, best);
    let r = down(&n.right, step, best);
    let mut run = 1;
    if let Some(c) = &n.left {
        if c.val == n.val + step && l + 1 > run {
            run = l + 1;
        }
    }
    if let Some(c) = &n.right {
        if c.val == n.val + step && r + 1 > run {
            run = r + 1;
        }
    }
    if run > *best {
        *best = run;
    }
    run
}

fn longest_with_step(t: &Option<Box<Node>>, step: i64) -> i64 {
    let mut best = 0;
    down(t, step, &mut best);
    best
}

fn main() {
    let depth = 20;
    let passes = 40;

    let mut state: i64 = 12345;
    let tree = build(depth, 0, &mut state);

    let mut checksum: i64 = 0;
    for d in 1..=passes {
        checksum = (checksum * 31 + longest_with_step(&tree, d as i64)) % 1_000_000_007;
    }

    println!("depth {} passes {} checksum {}", depth, passes, checksum);
}
