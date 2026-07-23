fn num_digits(x: i64) -> i64 {
    let mut d = 1i64;
    let mut t = x;
    while t >= 10 {
        d += 1;
        t /= 10;
    }
    d
}

fn pow10(k: i64) -> i64 {
    let mut r = 1i64;
    for _ in 0..k {
        r *= 10;
    }
    r
}

fn concat_val(a: i64, b: i64) -> i64 {
    a * pow10(num_digits(b)) + b
}

fn sort_desc(arr: &mut [i64], n: i64) {
    for i in 1..n {
        let mut j = i;
        while j > 0
            && concat_val(arr[(j - 1) as usize], arr[j as usize])
                < concat_val(arr[j as usize], arr[(j - 1) as usize])
        {
            arr.swap((j - 1) as usize, j as usize);
            j -= 1;
        }
    }
}

fn checksum(arr: &[i64], n: i64) -> i64 {
    let modv = 1000000007i64;
    let mut cs = 0i64;
    for i in 0..n {
        let x = arr[i as usize];
        let mut p = pow10(num_digits(x) - 1);
        while p > 0 {
            let d = (x / p) % 10;
            cs = (cs * 10 + d) % modv;
            p /= 10;
        }
    }
    cs
}

fn main() {
    let n: i64 = 500;
    let passes: i64 = 400;
    let mut base = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for c in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        base[c] = state % 1000;
    }
    let mut arr = vec![0i64; n as usize];
    let mut sink: i64 = 0;
    for p in 0..passes {
        arr[..n as usize].copy_from_slice(&base[..n as usize]);
        let idx = (p % n) as usize;
        arr[idx] = (arr[idx] + p + 1) % 1000;
        sort_desc(&mut arr, n);
        sink += checksum(&arr, n);
    }
    println!("{}", sink);
}
