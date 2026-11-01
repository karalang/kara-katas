"""Writes data/ for mini_infer: six OCaml programs, and data/jobs.txt with
the jobs that check them, ask for the types under the cursor, and check
one-line programs.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)
FILES = {}


def write(name, text):
    FILES[name] = text
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# A list library, written the way a course or a standard library starts:
# every function polymorphic, and the types the checker infers are the
# ones OCaml's List module documents.
write("lists.ml", '''\
(* A small list library. *)

let rec length l = match l with
  | [] -> 0
  | _ :: rest -> 1 + length rest

let rev l =
  let rec go acc l = match l with
    | [] -> acc
    | x :: xs -> go (x :: acc) xs
  in
  go [] l

let rec map f l = match l with
  | [] -> []
  | x :: xs -> f x :: map f xs

let rec filter p l = match l with
  | [] -> []
  | x :: xs -> if p x then x :: filter p xs else filter p xs

let rec fold_left f acc l = match l with
  | [] -> acc
  | x :: xs -> fold_left f (f acc x) xs

let rec fold_right f l acc = match l with
  | [] -> acc
  | x :: xs -> f x (fold_right f xs acc)

let rec assoc key l = match l with
  | [] -> None
  | (k, v) :: rest -> if k = key then Some v else assoc key rest

let rec range lo hi = if lo > hi then [] else lo :: range (lo + 1) hi

let rec zip a b = match (a, b) with
  | ([], []) -> Some []
  | (x :: xs, y :: ys) ->
    (match zip xs ys with
     | Some rest -> Some ((x, y) :: rest)
     | None -> None)
  | _ -> None

let rec insert cmp x l = match l with
  | [] -> [x]
  | y :: ys -> if cmp x y <= 0 then x :: l else y :: insert cmp x ys

let sort cmp l = fold_left (fun acc x -> insert cmp x acc) [] l

let rec exists p = function
  | [] -> false
  | x :: xs -> p x || exists p xs

let for_all p l = not (exists (fun x -> not (p x)) l)

let partition p l =
  fold_right (fun x (yes, no) -> if p x then (x :: yes, no) else (yes, x :: no)) l ([], [])

let concat_map f l = fold_right (fun x acc -> f x @ acc) l []

let rec uniq l = match l with
  | x :: rest -> uniq_from x rest
  | [] -> []
and uniq_from x rest = match rest with
  | [] -> [x]
  | y :: ys -> if x = y then uniq_from x ys else x :: uniq_from y ys

let sum = fold_left (fun a b -> a + b) 0
let join sep l = match l with
  | [] -> ""
  | x :: xs -> fold_left (fun acc s -> acc ^ sep ^ s) x xs

let squares = map (fun x -> x * x) (range 1 10)
let evens = filter (fun x -> x mod 2 = 0) squares
let total = sum evens
let sorted = sort compare [5; 3; 9; 1; 3]
let report = join ", " (map string_of_int (uniq sorted))
let pairs = zip [1; 2; 3] ["one"; "two"; "three"]
let lookup = match pairs with
  | Some ps -> assoc 2 ps
  | None -> None
''')

# Shapes and a canvas: records, variants with several arguments, record
# update, and the three warnings an editor shows while you type.
write("shapes.ml", '''\
type point = { x : int; y : int }

type shape =
  | Circle of point * int
  | Rect of point * point
  | Polygon of point list

type color = Red | Green | Blue | Rgb of int * int * int

type 'a styled = { shape : 'a; fill : color; stroke : int }

let origin = { x = 0; y = 0 }

let move dx dy p = { p with x = p.x + dx; y = p.y + dy }

let abs n = if n < 0 then - n else n

let rec poly_area2 pts = match pts with
  | a :: b :: rest -> (a.x * b.y - b.x * a.y) + poly_area2 (b :: rest)
  | _ -> 0

let area s = match s with
  | Circle (_, r) -> 3 * r * r
  | Rect (a, b) -> abs ((b.x - a.x) * (b.y - a.y))
  | Polygon pts -> abs (poly_area2 pts) / 2

let translate dx dy s = match s with
  | Circle (c, r) -> Circle (move dx dy c, r)
  | Rect (a, b) -> Rect (move dx dy a, move dx dy b)
  | Polygon pts -> Polygon (List_map.map (move dx dy) pts)

let rec map f l = match l with [] -> [] | x :: xs -> f x :: map f xs

let translate2 dx dy s = match s with
  | Circle (c, r) -> Circle (move dx dy c, r)
  | Rect (a, b) -> Rect (move dx dy a, move dx dy b)
  | Polygon pts -> Polygon (map (move dx dy) pts)

let color_name c = match c with
  | Red -> "red"
  | Green -> "green"
  | Rgb (r, g, b) -> "rgb(" ^ string_of_int r ^ "," ^ string_of_int g ^ "," ^ string_of_int b ^ ")"

let brightness c = match c with
  | Rgb (r, g, b) -> (r + g + b) / 3
  | _ -> 85

let is_primary c = match c with
  | Red -> true
  | Green -> true
  | Blue -> true
  | Rgb (255, 0, 0) -> true
  | Rgb (_, _, _) -> false
  | Blue -> false

let style s = { shape = s; fill = Blue; stroke = 1 }

let describe st =
  let a = area st.shape in
  let label = color_name st.fill in
  label ^ " shape of area " ^ string_of_int a

let canvas = map style [Circle (origin, 2); Rect (origin, { x = 3; y = 4 })]
let moved = map (fun st -> { st with shape = translate2 1 1 st.shape }) canvas
''')

# A JSON value, its printer, and path queries over it.
write("json.ml", '''\
type json =
  | Null
  | Bool of bool
  | Int of int
  | Str of string
  | List of json list
  | Obj of (string * json) list

type path_step = Key of string | Index of int

let rec quote_chars s = "\\"" ^ s ^ "\\""

let rec join_with f l = match l with
  | [] -> ""
  | [x] -> f x
  | x :: xs -> f x ^ "," ^ join_with f xs

let rec to_string j = match j with
  | Null -> "null"
  | Bool b -> string_of_bool b
  | Int n -> string_of_int n
  | Str s -> quote_chars s
  | List items -> "[" ^ join_with to_string items ^ "]"
  | Obj fields -> "{" ^ join_with field fields ^ "}"
and field kv = match kv with (k, v) -> quote_chars k ^ ":" ^ to_string v

let rec nth l n = match l with
  | [] -> None
  | x :: xs -> if n = 0 then Some x else nth xs (n - 1)

let rec member key fields = match fields with
  | [] -> None
  | (k, v) :: rest -> if k = key then Some v else member key rest

let rec get path j = match (path, j) with
  | ([], _) -> Some j
  | (Key k :: rest, Obj fields) ->
    (match member k fields with Some v -> get rest v | None -> None)
  | (Index i :: rest, List items) ->
    (match nth items i with Some v -> get rest v | None -> None)
  | (_ :: _, _) -> None

let int_at path j = match get path j with
  | Some (Int n) -> Some n
  | _ -> None

let order =
  Obj [("id", Int 1042);
       ("customer", Obj [("name", Str "Ada"); ("vip", Bool true)]);
       ("lines", List [Obj [("sku", Str "A-1"); ("qty", Int 2)];
                       Obj [("sku", Str "B-7"); ("qty", Int 1)]]);
       ("note", Null)]

let first_qty = int_at [Key "lines"; Index 0; Key "qty"] order
let text = to_string order
let missing = get [Key "lines"; Index 5] order

let rec total_qty items = match items with
  | [] -> 0
  | Obj fields :: rest ->
    (match member "qty" fields with
     | Some (Int q) -> q + total_qty rest
     | _ -> total_qty rest)
  | _ :: rest -> total_qty rest

let qty = match get [Key "lines"] order with
  | Some (List items) -> total_qty items
  | Some _ -> 0
''')

# An interpreter and a type checker for a tiny language: mutual
# recursion, a two-parameter result type, and environments as lists.
write("interp.ml", '''\
type ('a, 'e) result = Ok of 'a | Error of 'e

type expr =
  | Num of int
  | Bool of bool
  | Var of string
  | Add of expr * expr
  | Less of expr * expr
  | If of expr * expr * expr
  | Let of string * expr * expr
  | Fn of string * expr
  | Call of expr * expr

type value = VInt of int | VBool of bool | VClosure of string * expr * env
and env = (string * value) list

type ty = TInt | TBool | TFun of ty * ty

let bind r f = match r with
  | Ok v -> f v
  | Error e -> Error e

let rec lookup x env = match env with
  | [] -> Error ("unbound " ^ x)
  | (y, v) :: rest -> if x = y then Ok v else lookup x rest

let rec eval env e = match e with
  | Num n -> Ok (VInt n)
  | Bool b -> Ok (VBool b)
  | Var x -> lookup x env
  | Add (a, b) -> arith env a b (fun x y -> VInt (x + y))
  | Less (a, b) -> arith env a b (fun x y -> VBool (x < y))
  | If (c, t, f) ->
    bind (eval env c) (fun v -> match v with
      | VBool true -> eval env t
      | VBool false -> eval env f
      | _ -> Error "if: not a bool")
  | Let (x, a, b) -> bind (eval env a) (fun v -> eval ((x, v) :: env) b)
  | Fn (x, body) -> Ok (VClosure (x, body, env))
  | Call (f, a) -> bind (eval env f) (fun fv -> bind (eval env a) (fun av -> apply fv av))
and arith env a b k =
  bind (eval env a) (fun x -> bind (eval env b) (fun y -> match (x, y) with
    | (VInt m, VInt n) -> Ok (k m n)
    | _ -> Error "arith: not ints"))
and apply f a = match f with
  | VClosure (x, body, cenv) -> eval ((x, a) :: cenv) body
  | _ -> Error "call: not a function"

let rec type_of tenv e = match e with
  | Num _ -> Ok TInt
  | Bool _ -> Ok TBool
  | Var x -> lookup x tenv
  | Add (a, b) -> both tenv a b TInt TInt
  | Less (a, b) -> both tenv a b TInt TBool
  | If (c, t, f) ->
    bind (type_of tenv c) (fun tc ->
      if tc <> TBool then Error "if: condition" else
      bind (type_of tenv t) (fun tt ->
        bind (type_of tenv f) (fun tf ->
          if tt = tf then Ok tt else Error "if: branches")))
  | Let (x, a, b) -> bind (type_of tenv a) (fun ta -> type_of ((x, ta) :: tenv) b)
  | Fn (_, _) -> Error "fn: needs an annotation"
  | Call (f, a) ->
    bind (type_of tenv f) (fun tf -> bind (type_of tenv a) (fun ta -> match tf with
      | TFun (p, r) -> if p = ta then Ok r else Error "call: argument"
      | _ -> Error "call: not a function"))
and both tenv a b want res =
  bind (type_of tenv a) (fun ta -> bind (type_of tenv b) (fun tb ->
    if ta = want && tb = want then Ok res else Error "operands"))

let show r = match r with
  | Ok (VInt n) -> string_of_int n
  | Ok (VBool b) -> string_of_bool b
  | Ok (VClosure (x, _, _)) -> "<fun " ^ x ^ ">"
  | Error msg -> "error: " ^ msg

let prog = Let ("inc", Fn ("n", Add (Var "n", Num 1)),
                If (Less (Num 2, Num 3), Call (Var "inc", Num 41), Num 0))
let result = show (eval [] prog)
let bad = show (eval [] (Add (Num 1, Bool true)))
let checked = type_of [] (Add (Num 1, Num 2))
''')

# A bank ledger with the kind of mistakes a reviewer catches: each item
# fails on its own, and the items after it still check.
write("bank.ml", '''\
type account = { id : int; owner : string; balance : int }

type txn =
  | Deposit of int * int
  | Withdraw of int * int
  | Transfer of int * int * int

let open_account id owner = { id = id; owner = owner; balance = 0 }

let deposit acct amount = { acct with balance = acct.balance + amount }

let withdraw acct amount =
  if amount > acct.balance then None
  else Some { acct with balance = acct.balance - amount }

let fee acct = acct.balance * 2 / 100 ^ " EUR"

let label acct = acct.owner ^ " #" ^ acct.id

let rec find id accts = match accts with
  | [] -> None
  | a :: rest -> if a.id = id then Some a else find id rest

let apply accts t = match t with
  | Deposit (id, amt) -> find id accts
  | Withdraw (id) -> find id accts
  | Transfer (src, dst, amt) -> find src accts

let rec replace a accts = match accts with
  | [] -> []
  | b :: rest -> if b.id = a.id then a :: rest else b :: replace a rest

let post accts t = match t with
  | Deposit (id, amt) ->
    (match find id accts with
     | Some a -> replace (deposit a amt) accts
     | None -> accts)
  | Withdraw (id, amt) ->
    (match find id accts with
     | Some a -> (match withdraw a amt with Some b -> replace b accts | None -> accts)
     | None -> accts)
  | Transfer (src, dst, amt) -> accts

let summary accts = map (fun a -> a.owner) accts

let audit accts = List.length accts

let interest a = deposit a (a.balance / 100) 12

let rename a who = { a with name = who }

let bonus a = if a.balance > 1000 then deposit a 50

let close a = match a.balance with 0 -> Ok a | _ -> Error "balance"

let accounts = [open_account 1 "ada"; open_account 2 "grace"]
let after = post (post accounts (Deposit (1, 500))) (Withdraw (1, 200))
let rec balances accts = match accts with
  | [] -> []
  | a :: rest -> (a.owner, a.balance) :: balances rest
let final = balances after
''')

# A functional queue, a binary search tree used as a map, and a leftist
# heap: the data structures of a scheduler.
write("queue.ml", '''\
type 'a queue = { front : 'a list; back : 'a list }

let empty = { front = []; back = [] }

let push x q = { q with back = x :: q.back }

let rec rev_onto l acc = match l with
  | [] -> acc
  | x :: xs -> rev_onto xs (x :: acc)

let pop q = match q.front with
  | x :: f -> Some (x, { q with front = f })
  | [] ->
    (match rev_onto q.back [] with
     | [] -> None
     | x :: f -> Some (x, { front = f; back = [] }))

type ('k, 'v) tree =
  | Leaf
  | Node of ('k, 'v) tree * 'k * 'v * ('k, 'v) tree

let rec add k v t = match t with
  | Leaf -> Node (Leaf, k, v, Leaf)
  | Node (l, k2, v2, r) ->
    if k < k2 then Node (add k v l, k2, v2, r)
    else if k > k2 then Node (l, k2, v2, add k v r)
    else Node (l, k, v, r)

let rec find k t = match t with
  | Leaf -> None
  | Node (l, k2, v, r) ->
    if k = k2 then Some v else if k < k2 then find k l else find k r

let rec to_list t = match t with
  | Leaf -> []
  | Node (l, k, v, r) -> to_list l @ [(k, v)] @ to_list r

type 'a heap = E | H of int * 'a * 'a heap * 'a heap

let rank h = match h with E -> 0 | H (r, _, _, _) -> r

let make x a b =
  if rank a >= rank b then H (rank b + 1, x, a, b) else H (rank a + 1, x, b, a)

let rec merge h1 h2 = match (h1, h2) with
  | (E, h) -> h
  | (h, E) -> h
  | (H (_, x, a1, b1), H (_, y, a2, b2)) ->
    if x <= y then make x a1 (merge b1 h2) else make y a2 (merge h1 b2)
  | (E, E) -> E

let insert x h = merge (H (1, x, E, E)) h

let pop_min h = match h with
  | E -> None
  | H (_, x, a, b) -> Some (x, merge a b)

let rec drain h = match pop_min h with
  | None -> []
  | Some (x, rest) -> x :: drain rest

let jobs = add "build" 3 (add "test" 2 (add "deploy" 1 Leaf))
let order = to_list jobs
let next = find "test" jobs
let heap = insert 5 (insert 1 (insert 4 (insert 2 E)))
let ascending = drain heap
let q = push 3 (push 2 (push 1 empty))
let first = match pop q with Some (x, _) -> x | None -> 0
''')


def pos(name, needle, nth=1, off=0):
    """The 1-based line:column of the nth occurrence of needle, plus off."""
    text = FILES[name]
    i = -1
    for _ in range(nth):
        i = text.index(needle, i + 1)
    i += off
    line = text.count("\n", 0, i) + 1
    col = i - (text.rfind("\n", 0, i) + 1) + 1
    return f"{line}:{col}"


jobs = []
for name in FILES:
    jobs.append(f"check {name}")

jobs.append("hover lists.ml " + " ".join([
    pos("lists.ml", "go (x :: acc)"), pos("lists.ml", "acc) xs", 1, 0),
    pos("lists.ml", "f x :: map", 1, 2), pos("lists.ml", "(k, v) ::", 1, 1),
    pos("lists.ml", "insert cmp x acc", 1, 7), pos("lists.ml", "(yes, no)", 1, 1),
    pos("lists.ml", "uniq_from x rest", 1, 12), pos("lists.ml", "compare [5"),
    pos("lists.ml", "\"\""), "1:3",
    pos("lists.ml", "assoc 2 ps", 1, 8)]))
jobs.append("hover shapes.ml " + " ".join([
    pos("shapes.ml", "p.x + dx", 1, 2), pos("shapes.ml", "{ p with"),
    pos("shapes.ml", "st.shape", 1, 3), pos("shapes.ml", "label ^"),
    pos("shapes.ml", "style s", 1, 6), pos("shapes.ml", "Circle (origin, 2)"),
    pos("shapes.ml", "List_map")]))
jobs.append("hover json.ml " + " ".join([
    pos("json.ml", "join_with to_string", 1, 10), pos("json.ml", "kv = match"),
    pos("json.ml", "Key k :: rest", 1, 4), pos("json.ml", "int_at [Key", 1, 7),
    pos("json.ml", "Some (Int n)", 1, 10), pos("json.ml", "(\"note\", Null)", 1, 9)]))
jobs.append("hover interp.ml " + " ".join([
    pos("interp.ml", "bind r f"), pos("interp.ml", "(fun x y -> VInt", 1, 5),
    pos("interp.ml", "apply fv av", 1, 6), pos("interp.ml", "k m n", 1, 0),
    pos("interp.ml", "(x, ta) :: tenv", 1, 4), pos("interp.ml", "both tenv a b want res", 1, 14),
    pos("interp.ml", "VClosure (x, body, cenv)", 1, 19)]))
jobs.append("hover bank.ml " + " ".join([
    pos("bank.ml", "open_account id owner", 1, 13), pos("bank.ml", "acct.balance - amount", 1, 15),
    pos("bank.ml", "fee acct"), pos("bank.ml", "replace (deposit a amt)", 1, 9),
    pos("bank.ml", "(a.owner, a.balance)", 1, 1)]))
jobs.append("hover queue.ml " + " ".join([
    pos("queue.ml", "push x q", 1, 0), pos("queue.ml", "rev_onto q.back", 1, 9),
    pos("queue.ml", "Node (Leaf, k, v, Leaf)", 1, 12), pos("queue.ml", "to_list l @", 1, 10),
    pos("queue.ml", "make x a1", 1, 5), pos("queue.ml", "drain rest", 1, 6),
    pos("queue.ml", "\"build\""), pos("queue.ml", "Some (x, _)", 1, 6)]))

SNIPS = [
    # inference without errors
    "let id x = x\\nlet k x y = x\\nlet s f g x = f x (g x)",
    "let twice f x = f (f x)\\nlet add1 = twice (fun n -> n + 1)\\nlet hello = twice (fun s -> s ^ \"!\") \"hi\"",
    "let pair x y = (x, y)\\nlet swap (a, b) = (b, a)\\nlet p = swap (pair 1 \"one\")",
    "let rec even n = if n = 0 then true else odd (n - 1)\\nand odd n = if n = 0 then false else even (n - 1)",
    "let apply_all fs x = match fs with [] -> [] | f :: rest -> [f x]\\nlet r = apply_all [string_of_int] 3",
    "let flip f a b = f b a\\nlet sub = flip (fun a b -> a - b)\\nlet cons = flip (fun x l -> x :: l)",
    "let f = fun x -> let g y = (x, y) in g\\nlet h = f 1 \"a\"",
    "let compose f g = fun x -> f (g x)\\nlet len_str = compose string_of_int string_length",
    "let poly = let id x = x in (id 1, id true, id \"s\")",
    "type 'a box = Box of 'a\\nlet unbox b = match b with Box v -> v\\nlet nested = Box (Box 3)",
    "type ('a, 'b) either = Left of 'a | Right of 'b\\nlet lefts l = match l with Left x :: _ -> Some x | _ -> None",
    "let curry f a b = f (a, b)\\nlet uncurry f (a, b) = f a b",
    "let rec last l = match l with [] -> None | [x] -> Some x | _ :: rest -> last rest",
    "let x : int list = []\\nlet y = (fun (a : string) -> a) \"s\"",
    "let cmp (a : 'a) (b : 'a) = compare a b\\nlet c = cmp 1",
    "let rec loop n = if n > 0 then (print_int n; loop (n - 1))\\nlet () = loop 3",
    "let f x = match x with (0, y) -> y | (x, _) -> x\\nlet g = f (1, 2)",
    "type r = { name : string; age : int }\\nlet older p = { p with age = p.age + 1 }\\nlet ada = older { name = \"Ada\"; age = 36 }",
    "let rec fact n = if n <= 1 then 1 else n * fact (n - 1)\\nlet big = fact 10 > 1000 && not false",
    "let l = [1; 2] @ [3]\\nlet s = \"a\" ^ \"b\"\\nlet t = (l, s, -5, 7 mod 3)",
    # type errors
    "let x = 1 + true",
    "let f x = x + 1\\nlet y = f \"one\"",
    "let l = [1; \"two\"; 3]",
    "let b = if true then 1 else \"no\"",
    "let c = if 1 then 2 else 3",
    "let s = \"n = \" ^ 42",
    "let f (a, b) = a + b\\nlet r = f (1, 2, 3)",
    "let g x = x 1\\nlet r = g 2",
    "let three = 3\\nlet r = three 4",
    "let add a b = a + b\\nlet r = add 1 2 3",
    "let rec f x = f",
    "let self_apply = fun f -> f f",
    "let l = [[1]; [true]]",
    "let p : int * string = (1, 2)",
    "let f (x : string) = x + 1",
    "let m = match 3 with \"three\" -> 1 | _ -> 0",
    "let m = match [1] with (a, b) -> a",
    "let m = match Some 1 with Some \"x\" -> 1 | _ -> 0",
    "let m = match (1, true) with (a, 1) -> a | _ -> 0",
    "let u = print_string \"a\"; 5",
    "let w = if true then 5",
    "let h = fun x -> (x : int) ^ \"\"",
    "let rec map f l = match l with [] -> [] | x :: xs -> f x :: map xs",
    "let f x = (x, x)\\nlet g = f 1 + 1",
    "let rec show_all f l = match l with [] -> \"\" | x :: r -> f x ^ show_all f r\\nand show_ints l = show_all string_of_int l\\nand show_bools l = show_all string_of_bool l",
    "let opt = Some 1 + 1",
    "let wrong = fst (1, 2) ^ \"\"",
    "let n = max 1 \"2\"",
    # unbound names
    "let r = lenght [1]",
    "let rec length l = match l with [] -> 0 | _ :: t -> 1 + lenght t",
    "let total = summ 1 2\\nlet sum a b = a + b",
    "let v = Just 1",
    "let x : strng = \"a\"",
    "let v = undefined_thing",
    "let print_line s = print_strin s",
    # arity and constructors
    "let a = Some",
    "let a = None 1",
    "type t = Pair of int * int\\nlet a = Pair 1",
    "type t = Pair of int * int\\nlet a = Pair (1, 2, 3)",
    "type t = Pair of int * int\\nlet f p = match p with Pair x -> x",
    "type t = Pair of int * int\\nlet f p = match p with Pair _ -> 0",
    "let x : (int, int) list = []",
    "let x : int option option = Some None",
    "type 'a t = T of 'b",
    "type t = A of undefined",
    # records
    "type p = { x : int; y : int }\\nlet a = { x = 1; y = 2; x = 3 }",
    "type p = { x : int; y : int }\\nlet a = { x = 1 }",
    "type p = { x : int; y : int }\\nlet a = { x = 1; y = 2; z = 3 }",
    "type p = { x : int; y : int }\\nlet f r = r.z",
    "type p = { x : int; y : int }\\ntype q = { z : int }\\nlet a = { x = 1; z = 2 }",
    "type p = { x : int; y : int }\\nlet a = { x = \"1\"; y = 2 }",
    "type p = { x : int; y : int }\\nlet f r = r.x ^ \"\"",
    "type p = { x : int; y : int }\\nlet f r = match r with { x = 0; y } -> y | { x } -> x",
    "type a = { v : int }\\ntype b = { v : string }\\nlet f r = r.v",
    # patterns
    "let f (x, x) = x",
    "let f x = match x with (a, a) -> a",
    "let f x x = x",
    "let rec f = 3",
    "let rec (a, b) = (fun x -> x, fun y -> y)",
    # warnings
    "let f x = match x with 0 -> \"zero\" | 1 -> \"one\"",
    "let f x = match x with true -> 1",
    "let f l = match l with x :: _ -> x",
    "let f l = match l with [] -> 0 | [x] -> x",
    "let f s = match s with \"\" -> 0 | \"a\" -> 1",
    "let f p = match p with (true, false) -> 1 | (false, true) -> 2",
    "let f o = match o with Some (Some x) -> x | None -> 0",
    "let f x = match x with _ -> 1 | 0 -> 2",
    "let f x = match x with Some _ -> 1 | None -> 2 | Some 3 -> 3",
    "let f x = match x with y when y > 0 -> 1 | 0 -> 2",
    "let f x = match x with y when y > 0 -> 1 | _ -> 2 | 5 -> 3",
    "let g = let unused = 1 in let _ok = 2 in 3",
    "let g = let a = 1 and b = 2 in a",
    "let first (Some x) = x",
    "let Some y = Some 1",
    "type t = A | B | C\\nlet f = function A -> 1 | B -> 2",
    "type t = A | B | C\\nlet f x = match x with A -> 1 | _ -> 2 | C -> 3",
    "type p = { x : int; y : bool }\\nlet f r = match r with { y = true } -> 1",
    # lexing and syntax
    "let x = (* never closed",
    "let s = \"no end",
    "let x = 1 $ 2",
    "let x = \"bad \\\\q escape\"",
    "let x = 1 +",
    "let = 5",
    "let f x = match x with | -> 1",
    "type t = | lower",
    "let x = (1, 2",
    "let a = 1 let b = a +. 2",
]
for s in SNIPS:
    jobs.append("snip " + s)

with open(os.path.join("data", "jobs.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
