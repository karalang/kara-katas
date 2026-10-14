// LeetCode 631 -- Design Excel Sum Formula, bench mirror in Rust.
//
// The rebuild arm of excel.kara: every formula is the list of cells it
// reads, and after each write a depth-first walk orders the formula
// cells and recomputes them all. Same 2,000 operations, same 60 rounds,
// same output line.

struct Excel {
    width: i64,
    values: Vec<i64>,
    formulas: Vec<Option<Vec<i64>>>,
}

impl Excel {
    fn new(height: i64, width: char) -> Excel {
        let columns = width as i64 - 'A' as i64 + 1;
        let mut formulas: Vec<Option<Vec<i64>>> = Vec::new();
        for _ in 0..height * columns {
            formulas.push(None);
        }
        Excel { width: columns, values: vec![0; (height * columns) as usize], formulas }
    }

    fn set(&mut self, row: i64, column: char, val: i64) {
        let at = self.cell(row, column);
        self.values[at as usize] = val;
        self.formulas[at as usize] = None;
        self.recompute();
    }

    fn get(&self, row: i64, column: char) -> i64 {
        self.values[self.cell(row, column) as usize]
    }

    fn sum(&mut self, row: i64, column: char, numbers: &[String]) -> i64 {
        let at = self.cell(row, column);
        let mut reads: Vec<i64> = Vec::new();
        for range in numbers.iter() {
            let ends: Vec<&str> = range.split(':').collect();
            let (top, left) = self.position(ends[0]);
            let (bottom, right) = self.position(ends[ends.len() - 1]);
            for r in top..bottom + 1 {
                for c in left..right + 1 {
                    reads.push(r * self.width + c);
                }
            }
        }
        self.formulas[at as usize] = Some(reads);
        self.recompute();
        self.values[at as usize]
    }

    fn cell(&self, row: i64, column: char) -> i64 {
        (row - 1) * self.width + (column as i64 - 'A' as i64)
    }

    // The zero-based row and column of a name such as `B12`.
    fn position(&self, name: &str) -> (i64, i64) {
        let column = name.chars().next().unwrap() as i64 - 'A' as i64;
        let row: i64 = name[1..].parse().unwrap();
        (row - 1, column)
    }

    fn recompute(&mut self) {
        let mut seen = vec![false; self.values.len()];
        let mut order: Vec<i64> = Vec::new();
        for at in 0..self.values.len() as i64 {
            visit(&self.formulas, at, &mut seen, &mut order);
        }
        for at in order.iter() {
            if let Some(reads) = &self.formulas[*at as usize] {
                let mut total = 0;
                for source in reads.iter() {
                    total += self.values[*source as usize];
                }
                self.values[*at as usize] = total;
            }
        }
    }
}

// Append `at` to `order` after every cell its formula reads.
fn visit(formulas: &[Option<Vec<i64>>], at: i64, seen: &mut Vec<bool>, order: &mut Vec<i64>) {
    if seen[at as usize] {
        return;
    }
    seen[at as usize] = true;
    if let Some(reads) = &formulas[at as usize] {
        for source in reads.iter() {
            visit(formulas, *source, seen, order);
        }
    }
    order.push(at);
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(index: i64) -> char {
    (b'A' + index as u8) as char
}

struct Op {
    kind: i64,
    row: i64,
    column: char,
    val: i64,
    ranges: Vec<String>,
}

fn make_ops(count: i64, seed: &mut i64) -> Vec<Op> {
    let mut ops: Vec<Op> = Vec::new();
    for _ in 0..count {
        let mut kind = next_random(seed) % 3;
        let row = 1 + next_random(seed) % 26;
        let column = letter(next_random(seed) % 26);
        let mut val = 0;
        let mut ranges: Vec<String> = Vec::new();
        if kind == 0 {
            val = next_random(seed) % 2001 - 1000;
        } else if kind == 1 && row > 1 {
            for _ in 0..1 + next_random(seed) % 3 {
                let top = 1 + next_random(seed) % (row - 1);
                let left = next_random(seed) % 26;
                let bottom = (top + next_random(seed) % 2).min(row - 1);
                let right = (left + next_random(seed) % 2).min(25);
                if top == bottom && left == right {
                    ranges.push(format!("{}{}", letter(left), top));
                } else {
                    ranges.push(format!("{}{}:{}{}", letter(left), top, letter(right), bottom));
                }
            }
        } else {
            kind = 2;
        }
        ops.push(Op { kind, row, column, val, ranges });
    }
    ops
}

fn main() {
    let mut seed: i64 = 631;
    let ops = make_ops(2000, &mut seed);
    let rounds = 60;
    let mut sums = 0;
    let mut checksum: i64 = 0;
    let mut total: i64 = 0;
    for _ in 0..rounds {
        let mut sheet = Excel::new(26, 'Z');
        for op in ops.iter() {
            let mut result = 0;
            if op.kind == 0 {
                sheet.set(op.row, op.column, op.val);
            } else if op.kind == 1 {
                result = sheet.sum(op.row, op.column, &op.ranges);
                sums += 1;
            } else {
                result = sheet.get(op.row, op.column);
            }
            checksum = ((checksum * 31 + result) % 1000000007 + 1000000007) % 1000000007;
        }
        for row in 1..27 {
            for c in 0..26 {
                total += sheet.get(row, letter(c));
            }
        }
    }
    println!(
        "{} operations, {} rounds ({} sums): checksum {}, sheet total {}",
        ops.len(), rounds, sums, checksum, total
    );
}
