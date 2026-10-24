// Benchmark: LeetCode #972 Equal Rational Numbers -- the ★ arm, both as
// fractions in lowest terms, on 1000 random pairs of strings. Mirrors
// is_rational_equal.kara, .c, .py and go-seq/.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn fraction(s: &str) -> (i64, i64) {
    let (mut whole, mut shift, mut rep, mut nines) = (0i64, 1i64, 0i64, 0i64);
    let mut part = 0;
    for c in s.bytes() {
        if c == b'.' {
            part = 1;
        } else if c == b'(' {
            part = 2;
        } else if c != b')' {
            let d = (c - b'0') as i64;
            if part == 2 {
                rep = rep * 10 + d;
                nines = nines * 10 + 9;
            } else {
                whole = whole * 10 + d;
                if part == 1 {
                    shift *= 10;
                }
            }
        }
    }
    let (num, den) = if nines == 0 { (whole, shift) } else { (whole * nines + rep, shift * nines) };
    let g = gcd(num, den);
    (num / g, den / g)
}

fn is_rational_equal(s: &str, t: &str) -> bool {
    fraction(s) == fraction(t)
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

#[derive(Clone)]
struct Num {
    int: i64,
    non: String,
    rep: String,
    dot: bool,
}

fn digits(len: i64, rng: &mut Rng) -> String {
    (0..len).map(|_| char::from(b'0' + (rng.next() % 10) as u8)).collect()
}

fn text(x: &Num) -> String {
    let mut s = x.int.to_string();
    if x.dot || !x.non.is_empty() || !x.rep.is_empty() {
        s.push('.');
    }
    s.push_str(&x.non);
    if !x.rep.is_empty() {
        s.push('(');
        s.push_str(&x.rep);
        s.push(')');
    }
    s
}

fn random_num(rng: &mut Rng) -> Num {
    let len = 1 + rng.next() % 4;
    let mut int = rng.next() % 10;
    for _ in 1..len {
        int = int * 10 + rng.next() % 10;
    }
    let nlen = rng.next() % 5;
    let non = digits(nlen, rng);
    let rep = if rng.next() % 3 == 0 {
        String::new()
    } else {
        let rlen = 1 + rng.next() % 4;
        digits(rlen, rng)
    };
    let dot = rng.next() % 2 == 0;
    Num { int, non, rep, dot }
}

fn variant(x: &Num, rng: &mut Rng) -> Num {
    let mut y = x.clone();
    let steps = 1 + rng.next() % 3;
    for _ in 0..steps {
        let kind = rng.next() % 7;
        let r = y.rep.len();
        if kind == 0 && r > 0 && y.non.len() < 4 {
            let first = y.rep[..1].to_string();
            y.non.push_str(&first);
            y.rep = format!("{}{}", &y.rep[1..], first);
        } else if kind == 1 && r > 0 && 2 * r <= 4 {
            y.rep = y.rep.repeat(2);
        } else if kind == 2 && r == 0 && y.non.len() < 4 {
            y.non.push('0');
        } else if kind == 3 && r == 0 {
            y.rep = "0".to_string();
        } else if kind == 4 && r == 0 {
            if !y.non.is_empty() && !y.non.ends_with('0') {
                let last = y.non.pop().unwrap() as u8;
                y.non.push(char::from(last - 1));
                y.rep = "9".to_string();
            } else if y.non.is_empty() && y.int > 0 {
                y.int -= 1;
                y.rep = "9".to_string();
            }
        } else if kind == 5 && r > 0 && y.rep.bytes().all(|c| c == b'0') {
            y.rep.clear();
            y.dot = true;
        } else if kind == 6 && r % 2 == 0 && r > 0 && y.rep[..r / 2] == y.rep[r / 2..] {
            y.rep.truncate(r / 2);
        }
    }
    y
}

fn nudge(s: &str, rng: &mut Rng) -> String {
    let b = s.as_bytes();
    let places: Vec<usize> = (0..b.len()).filter(|&i| b[i].is_ascii_digit()).collect();
    let at = places[(rng.next() % places.len() as i64) as usize];
    let old = (b[at] - b'0') as i64;
    let mut new = rng.next() % 9;
    if new >= old {
        new += 1;
    }
    if at == 0 && new == 0 && b.len() > 1 && b[1].is_ascii_digit() {
        new = 1 + old % 9;
        if new == old {
            new = 9;
        }
    }
    format!("{}{}{}", &s[..at], new, &s[at + 1..])
}

fn random_pair(c: usize, rng: &mut Rng) -> (String, String) {
    let x = random_num(rng);
    if c % 3 == 0 {
        let y = variant(&x, rng);
        (text(&x), text(&y))
    } else if c % 3 == 1 {
        let y = text(&variant(&x, rng));
        (text(&x), nudge(&y, rng))
    } else {
        let y = random_num(rng);
        (text(&x), text(&y))
    }
}

fn main() {
    let rounds = 1000;
    let count = 1000;
    let mut rng = Rng(972);
    let pairs: Vec<(String, String)> = (0..count).map(|c| random_pair(c, &mut rng)).collect();
    let mut equal: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let (s, t) = &pairs[(r + i) % count];
            if is_rational_equal(s, t) {
                equal += 1;
                check = (check * 2 + 1) % 1000000007;
            } else {
                check = check * 2 % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} pairs: {equal} equal, checksum {check}");
}
