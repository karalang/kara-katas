// LeetCode #1634: Add Two Polynomials Represented as Linked Lists -- the
// bench's Rust mirror: the ★ arm on 10 random pairs of polynomials with
// powers below 400000, all drawn first as terms; each pair is built into
// two lists of `Option<Box<PolyNode>>` and added.

struct PolyNode {
    coefficient: i64,
    power: i64,
    next: Option<Box<PolyNode>>,
}

fn add_poly(poly1: Option<Box<PolyNode>>, poly2: Option<Box<PolyNode>>) -> Option<Box<PolyNode>> {
    let mut head = Box::new(PolyNode { coefficient: 0, power: 0, next: None });
    let mut tail = &mut head;
    let (mut a, mut b) = (poly1, poly2);
    loop {
        let (coefficient, power) = match (a.take(), b.take()) {
            (Some(x), Some(y)) if x.power == y.power => {
                a = x.next;
                b = y.next;
                (x.coefficient + y.coefficient, x.power)
            }
            (Some(x), Some(y)) if x.power < y.power => {
                a = Some(x);
                b = y.next;
                (y.coefficient, y.power)
            }
            (Some(x), rest) => {
                b = rest;
                a = x.next;
                (x.coefficient, x.power)
            }
            (None, Some(y)) => {
                b = y.next;
                (y.coefficient, y.power)
            }
            (None, None) => break,
        };
        if coefficient != 0 {
            tail.next = Some(Box::new(PolyNode { coefficient, power, next: None }));
            tail = tail.next.as_mut().unwrap();
        }
    }
    head.next
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn from_terms(terms: &[[i64; 2]]) -> Option<Box<PolyNode>> {
    let mut head: Option<Box<PolyNode>> = None;
    for term in terms.iter().rev() {
        head = Some(Box::new(PolyNode { coefficient: term[0], power: term[1], next: head }));
    }
    head
}

fn random_terms(seed: &mut i64) -> Vec<[i64; 2]> {
    let mut terms = Vec::new();
    for power in (0..400000).rev() {
        if next_random(seed) % 2 == 0 {
            let mut coefficient = next_random(seed) % 6 - 3;
            if coefficient >= 0 {
                coefficient += 1;
            }
            terms.push([coefficient, power]);
        }
    }
    terms
}

fn main() {
    let mut seed: i64 = 1634;
    let mut pairs = Vec::new();
    for _ in 0..10 {
        let poly1 = random_terms(&mut seed);
        let poly2 = random_terms(&mut seed);
        pairs.push((poly1, poly2));
    }
    let mut check: i64 = 0;
    let mut terms: i64 = 0;
    for (poly1, poly2) in &pairs {
        let mut node = add_poly(from_terms(poly1), from_terms(poly2));
        while let Some(mut n) = node {
            terms += 1;
            check = ((check * 31 + n.coefficient + 1000000) % 1000000007 * 31 + n.power) % 1000000007;
            node = n.next.take();
        }
    }
    println!("10 pairs of up to 400000 terms: {} terms, checksum {}", terms, check);
}
