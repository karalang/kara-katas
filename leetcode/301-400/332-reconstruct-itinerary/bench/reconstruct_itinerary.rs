// Benchmark harness for LeetCode #332 — Hierholzer Eulerian path.
// Mirrors reconstruct_itinerary.kara algorithm-for-algorithm.
//
// NOTE on the adjacency build: this uses the idiomatic `entry().or_default()
// .push()`, which is O(1) amortized. The Kara mirror cannot express that —
// `m[k].push(x)` is rejected by codegen (kara ledger B-2026-07-25-5, open), so
// it must do get-copy-push-insert, and because `Map.get` yields a copy that is
// O(degree) per edge. See ../README.md § Benchmarks; the gap is part of what
// these numbers measure.

use std::collections::HashMap;

fn visit(
    adj: &HashMap<String, Vec<String>>,
    cursor: &mut HashMap<String, i64>,
    airport: &str,
    route: &mut Vec<String>,
) {
    loop {
        let used = *cursor.get(airport).unwrap_or(&0);
        let next = match adj.get(airport) {
            Some(d) if (used as usize) < d.len() => d[used as usize].clone(),
            _ => break,
        };
        cursor.insert(airport.to_string(), used + 1);
        visit(adj, cursor, &next, route);
    }
    route.push(airport.to_string());
}

fn find_itinerary(froms: &[String], tos: &[String], rot: i64) -> Vec<String> {
    let e = froms.len() as i64;
    let mut adj: HashMap<String, Vec<String>> = HashMap::new();
    for i in 0..e {
        let idx = ((i + rot) % e) as usize;
        adj.entry(froms[idx].clone())
            .or_default()
            .push(tos[idx].clone());
    }

    for d in adj.values_mut() {
        d.sort();
    }

    let mut cursor: HashMap<String, i64> = HashMap::new();
    let mut route: Vec<String> = Vec::new();
    visit(&adj, &mut cursor, "JFK", &mut route);

    route.reverse();
    route
}

fn main() {
    let m: i64 = 40;
    let l: i64 = 24;
    let iters: i64 = 250;

    let mut froms: Vec<String> = Vec::new();
    let mut tos: Vec<String> = Vec::new();
    for j in 0..m {
        let mut prev = String::from("JFK");
        for k in 0..l {
            let cur = format!("A{}", j * l + k);
            froms.push(prev.clone());
            tos.push(cur.clone());
            prev = cur;
        }
        froms.push(prev);
        tos.push(String::from("JFK"));
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let path = find_itinerary(&froms, &tos, it);
        for (i, s) in path.iter().enumerate() {
            let cs: i64 = s.bytes().map(|b| b as i64).sum();
            sink += (i as i64 + 1) * cs;
        }
    }
    println!("{}", sink);
}
