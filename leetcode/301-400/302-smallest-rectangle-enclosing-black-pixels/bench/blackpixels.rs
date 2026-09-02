// LeetCode 302 benchmark lane — Rust mirror of blackpixels.kara.
//
// Same algorithm: 4-way binary search on the row/column projections. Written as
// plain index loops rather than iterator combinators so the shape matches the
// Kara and C mirrors — an `any()` chain would be measuring a different thing.

struct Image { data: Vec<u8>, w: i64, h: i64 }

impl Image {
    #[inline]
    fn at(&self, r: i64, c: i64) -> u8 { self.data[(r * self.w + c) as usize] }

    fn row_has_black(&self, r: i64) -> bool {
        let mut c = 0;
        while c < self.w { if self.at(r, c) == 1 { return true; } c += 1; }
        false
    }
    fn col_has_black(&self, c: i64) -> bool {
        let mut r = 0;
        while r < self.h { if self.at(r, c) == 1 { return true; } r += 1; }
        false
    }

    fn first_black_row(&self, mut lo: i64, mut hi: i64) -> i64 {
        while lo < hi { let m = lo + (hi - lo) / 2; if self.row_has_black(m) { hi = m } else { lo = m + 1 } }
        lo
    }
    fn first_white_row(&self, mut lo: i64, mut hi: i64) -> i64 {
        while lo < hi { let m = lo + (hi - lo) / 2; if self.row_has_black(m) { lo = m + 1 } else { hi = m } }
        lo
    }
    fn first_black_col(&self, mut lo: i64, mut hi: i64) -> i64 {
        while lo < hi { let m = lo + (hi - lo) / 2; if self.col_has_black(m) { hi = m } else { lo = m + 1 } }
        lo
    }
    fn first_white_col(&self, mut lo: i64, mut hi: i64) -> i64 {
        while lo < hi { let m = lo + (hi - lo) / 2; if self.col_has_black(m) { lo = m + 1 } else { hi = m } }
        lo
    }

    fn min_area(&self, x: i64, y: i64) -> i64 {
        let top = self.first_black_row(0, x + 1);
        let bottom = self.first_white_row(x + 1, self.h);
        let left = self.first_black_col(0, y + 1);
        let right = self.first_white_col(y + 1, self.w);
        (bottom - top) * (right - left)
    }
}

fn main() {
    let n: i64 = 4096;
    let queries: i64 = 1200;
    let mut data = vec![0u8; (n * n) as usize];

    let (r0, c0) = (n / 2, n / 2);
    for r in 0..40 { for c in 0..40 { data[((r0 + r) * n + (c0 + c)) as usize] = 1; } }
    for k in 0..25 { data[((r0 + 40 + k) * n + (c0 + 20)) as usize] = 1; }
    let img = Image { data, w: n, h: n };

    let mut checksum: i64 = 0;
    for q in 0..queries {
        let sx = r0 + q % 40;
        let sy = c0 + (q * 7) % 40;
        checksum = (checksum * 31 + img.min_area(sx, sy)) % 1000000007;
    }
    println!("queries {} checksum {}", queries, checksum);
}
