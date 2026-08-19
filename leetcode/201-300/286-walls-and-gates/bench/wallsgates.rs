// Rust mirror of wallsgates_seq.kara — see ../README.md § Benchmarks.
// Same LCG, same board parameters, same flat queue, same build-once/punch-many
// shape. Built twice by bench.sh: once plain (`rustc -O`) and once with
// overflow checks on, which is the equal-safety comparator against Kara's
// always-checked arithmetic.

const INF: i64 = 2147483647;

fn make_board(b: i64, n: i64) -> Vec<i64> {
    let mut g = Vec::with_capacity(n as usize);
    let mut s = 777i64 + b * 1013;
    for _ in 0..n {
        s = (s.wrapping_mul(1103515245) + 12345) % 2147483648;
        let roll = s % 100;
        g.push(if roll < 20 { -1 } else if roll < 21 { 0 } else { INF });
    }
    g
}

fn solve(template: &[i64], r: i64, c: i64) -> (i64, i64) {
    let n = (r * c) as usize;
    let mut g = template.to_vec();

    let mut q: Vec<i64> = Vec::with_capacity(n);
    for k in 0..n {
        if g[k] == 0 {
            q.push(k as i64);
        }
    }

    let mut head = 0usize;
    while head < q.len() {
        let cell = q[head];
        head += 1;
        let row = cell / c;
        let col = cell % c;
        let d = g[cell as usize] + 1;
        let relax = |q: &mut Vec<i64>, g: &mut Vec<i64>, nb: i64| {
            if g[nb as usize] == INF {
                g[nb as usize] = d;
                q.push(nb);
            }
        };
        if row > 0 { relax(&mut q, &mut g, cell - c); }
        if row < r - 1 { relax(&mut q, &mut g, cell + c); }
        if col > 0 { relax(&mut q, &mut g, cell - 1); }
        if col < c - 1 { relax(&mut q, &mut g, cell + 1); }
    }

    let mut total = 0i64;
    let mut unreachable = 0i64;
    for j in 0..n {
        if g[j] == INF { unreachable += 1; } else if g[j] > 0 { total += g[j]; }
    }
    (total, unreachable)
}

fn run_board(b: i64, r: i64, c: i64, reps: i64) -> (i64, i64) {
    let template = make_board(b, r * c);
    let mut total = 0i64;
    let mut unreachable = 0i64;
    for _ in 0..reps {
        let (t, u) = solve(&template, r, c);
        total += t;
        unreachable += u;
    }
    (total, unreachable)
}

fn main() {
    let (boards, r, c, reps) = (16i64, 512i64, 512i64, 8i64);
    let mut total = 0i64;
    let mut unreachable = 0i64;
    for b in 0..boards {
        let (t, u) = run_board(b, r, c, reps);
        total += t;
        unreachable += u;
    }
    println!("{} {}", total, unreachable);
}
