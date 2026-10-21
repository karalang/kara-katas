# Writes data/: the HCL files of a small company's infrastructure repo
# (Terraform, Vault policies, a Nomad job, a Consul agent, a Packer
# template), the decoder and lexer fixtures of pyhcl's tests (copied from
# hcl_fixtures/), files that break the lexer, the parser and the actions,
# and jobs.tsv, the jobs mini_pyhcl runs. Everything is fixed, so the
# files never change.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FILES = {}

FILES["infra/terraform/variables.tf"] = '''\
variable "region" {
  description = "AWS region for every resource"
  default     = "eu-west-1"
}

variable "instance_count" {
  default = 3
}

variable "instance_type" {
  type    = "string"
  default = "t3.small"
}

variable "allowed_cidrs" {
  type    = "list"
  default = ["10.0.0.0/16", "192.168.10.0/24"]
}

variable "tags" {
  type = "map"
  default = {
    team    = "platform"
    billing = "shop-42"
  }
}

variable "db_password" {
  description = "set from the CI secret store"
}
'''

FILES["infra/terraform/main.tf"] = '''\
# The shop's web tier: instances behind a load balancer, one database.
terraform {
  required_version = ">= 0.11.0"
  backend "s3" {
    bucket = "shop-terraform-state"
    key    = "web/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region  = "${var.region}"
  version = "~> 2.70"
}

provider "aws" {
  alias  = "us"
  region = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  count         = "${var.instance_count}"
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "${var.instance_type}"
  subnet_id     = "${element(module.vpc.public_subnets, count.index)}"

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }

  tags = "${merge(var.tags, map("Name", "web-${count.index + 1}"))}"

  user_data = <<EOF
#!/bin/sh
apt-get update
apt-get install -y nginx
echo "web ${count.index}" > /var/www/html/index.html
EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb" "web" {
  name               = "shop-web"
  load_balancer_type = "application"
  subnets            = ["${module.vpc.public_subnets}"]
  idle_timeout       = 60
}

resource "aws_lb_target_group" "web" {
  name     = "shop-web"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "${module.vpc.vpc_id}"

  health_check {
    path                = "/healthz"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_security_group" "web" {
  name = "shop-web"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "orders" {
  allocated_storage       = 50
  engine                  = "postgres"
  engine_version          = "11.9"
  instance_class          = "db.t3.medium"
  name                    = "orders"
  username                = "shop"
  password                = "${var.db_password}"
  backup_retention_period = 7
  multi_az                = false
  max_allocated_storage   = 50 * 4
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "2.78.0"
  name   = "shop"
  cidr   = "10.0.0.0/16"
  azs    = ["eu-west-1a", "eu-west-1b"]
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
}

module "dns" {
  source = "./modules/dns"
  zone   = "shop.example"
}
'''

FILES["infra/terraform/outputs.tf"] = '''\
output "lb_dns_name" {
  value = "${aws_lb.web.dns_name}"
}

output "instance_ips" {
  value     = ["${aws_instance.web.*.private_ip}"]
  sensitive = false
}

output "db_endpoint" {
  value       = "${aws_db_instance.orders.endpoint}"
  description = "where the order service connects"
  sensitive   = true
}
'''

FILES["infra/terraform/main.tf.json"] = '''\
{
  "resource": {
    "aws_s3_bucket": {
      "assets": {
        "bucket": "shop-assets",
        "acl": "private",
        "versioning": {"enabled": true},
        "lifecycle_rule": [
          {"id": "old", "enabled": true, "expiration": {"days": 90}}
        ]
      }
    }
  },
  "output": {
    "assets_bucket": {"value": "${aws_s3_bucket.assets.id}"}
  },
  "variable": {
    "cdn_ttl": {"default": 3600.5, "description": "seconds \\u00e0 la carte"}
  }
}
'''

FILES["infra/vault/admin.hcl"] = '''\
# Operators manage everything but the root token.
path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "auth/token/root" {
  capabilities = ["deny"]
}

path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/data/payments/*" {
  capabilities = ["read", "list"]
}
'''

FILES["infra/vault/ci.hcl"] = '''\
// The CI runners read deploy keys and nothing else.
path "secret/data/ci/*" {
  capabilities = ["read"]
}

path "secret/metadata/ci/*" {
  capabilities = ["list"]
}

path "secret/data/ci/prod-signing" {
  capabilities = ["deny"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "transit/encrypt/ci" {
  capabilities = ["update"]
}
'''

FILES["infra/nomad/web.nomad"] = '''\
job "web" {
  datacenters = ["eu-west-1a", "eu-west-1b"]
  type        = "service"
  priority    = 60

  update {
    max_parallel     = 1
    min_healthy_time = "10s"
    healthy_deadline = "3m"
  }

  group "frontend" {
    count = 3

    task "nginx" {
      driver = "docker"
      config {
        image = "nginx:1.25"
        port_map {
          http = 80
        }
      }
      resources {
        cpu    = 500
        memory = 256
      }
    }

    task "log-shipper" {
      driver = "docker"
      config {
        image = "timberio/vector:0.34.1-alpine"
      }
      resources {
        cpu    = 100
        memory = 64
      }
    }
  }

  group "api" {
    count = 2

    task "orders" {
      driver = "exec"
      config {
        command = "/usr/local/bin/orders"
        args    = ["--port", "${NOMAD_PORT_http}", "--db", "orders.service.consul"]
      }
      env {
        RUST_LOG = "info"
        WORKERS  = 4
      }
      resources {
        cpu    = 1000
        memory = 512
      }
    }
  }
}
'''

FILES["infra/consul/agent.hcl"] = '''\
datacenter = "eu-west-1"
data_dir   = "/opt/consul"
log_level  = "INFO"
server     = true
bootstrap_expect = 3
retry_join = ["provider=aws tag_key=consul tag_value=server"]

ui_config {
  enabled = true
}

ports {
  grpc  = 8502
  https = -1
}

telemetry {
  prometheus_retention_time = "24h"
  disable_hostname          = true
}

acl = {
  enabled        = true
  default_policy = "deny"
  tokens {
    agent = "00000000-0000-0000-0000-000000000000"
  }
}

performance {
  raft_multiplier = 1
}

limits {
  http_max_conns_per_client = 200
  rpc_rate                  = 1e3
  rpc_max_burst             = 1.5e3
}
'''

FILES["infra/packer/base.pkr.hcl"] = '''\
variable "aws_region" {
  type    = "string"
  default = "eu-west-1"
}

source "amazon-ebs" "base" {
  region        = "${var.aws_region}"
  instance_type = "t3.micro"
  ssh_username  = "ubuntu"
  ami_name      = "shop-base-{{timestamp}}"
}

build {
  sources = ["source.amazon-ebs.base"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y unattended-upgrades",
    ]
  }

  provisioner "file" {
    source      = "files/motd"
    destination = "/tmp/motd"
  }
}
'''

# Values the grammar and its actions handle in their own way.
FILES["cases/numbers.hcl"] = '''\
dec       = 42
neg       = -17
hex       = 0x1F
neghex    = -0xff
float     = 3.25
lead      = .5
trail     = 2.
negf      = -0.0
sci       = 1e3
scineg    = 2.5e-2
sciplus   = 4E+2
huge      = 1e400
sum       = 1 + 2
mixed     = 1 + 2.5
diff      = 10 - 3 - 2
prod      = 6 * 7
quot      = 7 / 2
exact     = 8 / 4
chain     = 2 + 3 * 4
negmul    = -2 * -3
'''

FILES["cases/strings.hcl"] = '''\
plain   = "hello"
escaped = "say \\"hi\\" now"
slash   = "C:\\\\temp\\\\new"
tab     = "a\\tb"
interp  = "${var.name}-${lookup(var.map, "key")}"
nested  = "${format("%s-%s", "a", "${var.b}")}"
unicode = "caf\u00e9 \u2603 \U0001F600"
multi   = "line one
line two"
empty   = ""
bare    = some.identifier-name
truthy  = true
falsy   = false
'''

FILES["cases/heredocs.hcl"] = '''\
plain = <<EOT
line one
  line two
EOT
tabbed = <<-EOT
\tindented
\t\tdeeper
\tEOT
same_line = <<EOT
first
lastEOT
empty = <<EOT
EOT
after = "done"
'''

FILES["cases/crlf_heredoc.hcl"] = 'a = <<EOF\r\nwindows\r\nlines\r\nEOF\r\nb = 1\r\n'

FILES["cases/keys.hcl"] = '''\
"quoted key" = 1
dotted.key = 2
dashed-key = 3
colon: "value"
list_colon: [1, 2]
obj_colon: { a = 1 }
'''

FILES["cases/expressions.hcl"] = '''\
cond      = var.env == "prod" ? 3 : 1
cmp       = count.index >= 2
cmp2      = 5 < var.max
fn_list   = concat(var.a, var.b)
fn_lists  = concat(["a"], ["b"], ["c"])
splat     = [aws_instance.web.*.id, aws_instance.db.*.id]
splat2    = [var.first, aws_instance.web.*.id]
index     = aws_subnet.private[0].id
index_key = aws_subnet.private[var.az].id
bracket   = foo[bar]
'''

FILES["cases/lists.hcl"] = '''\
empty    = []
nums     = [1, 2, 3,]
objects  = [{ name = "a" }, { name = "b" }]
comments = [
  "one", # first
  "two", // second
  "three", /* third */
]
paren    = ()
'''

FILES["cases/duplicates.hcl"] = '''\
name = "first"
name = "second"

service "web" {
  port = 80
}

service "web" {
  tags = ["edge"]
}

service "db" {
  port = 5432
}

check {
  interval = "10s"
}

check {
  interval = "30s"
}

inner {
  x = 1
  x = 2
  block "a" { v = 1 }
  block "a" { w = 2 }
  block "b" { v = 3 }
}

top "t" { a = 1 }
top = "now a string"
'''

FILES["cases/merges.hcl"] = '''\
group {
  a = 1
}
group "x" {
  b = 2
}
group "y" "z" {
  c = 3
}

scalar = "s"
scalar "k" {
  d = 4
}
'''

FILES["cases/comments.hcl"] = '''\
# A hash comment
// A slash comment
/* A block
   comment */
key = "value" # trailing
block {
  # inside
  inner = 1
}
'''

FILES["cases/fn_nested.hcl"] = 'fn = join(",", list("a", "b"))\n'
FILES["cases/fn_objs.hcl"] = 'fn_objs = merge({a = 1}, {b = 2})\n'
FILES["cases/expand.hcl"] = 'expand = max([1, 2, 3]...)\n'
FILES["cases/func_cond.hcl"] = 'func_cond = var.x == 1 ? max(1, 2) : min(3, 4)\n'
FILES["cases/mixed_list.hcl"] = 'mixed = ["a", 1, true, 1.5]\n'
FILES["cases/trueish.hcl"] = "trueish = trueish\n"
FILES["cases/cond_bool.hcl"] = "cond_bool = var.debug != true ? false : true\n"
FILES["cases/nested_lists.hcl"] = "nested = [[1, 2], [3]]\n"
FILES["cases/arith_keys.hcl"] = '''\
x+1 = "plus"
'''

FILES["cases/arith_keys2.hcl"] = '''\
config {
  x+1 = "plus"
  2*y = "times"
}
'''

FILES["cases/flatten_number.hcl"] = '''\
v = join("", [1, 2])
'''

FILES["cases/zero_div.hcl"] = '''\
ok = 1
bad = 1 / 0
'''

FILES["cases/zero_div_float.hcl"] = '''\
bad = 1.5 / 0
'''

FILES["cases/float_exp.hcl"] = '''\
v = 100000000000000000.0e2
'''

FILES["cases/tuple_concat.hcl"] = '''\
v = a+1 ? "x" : "y"
'''

FILES["cases/attr_error.hcl"] = '''\
d = "text"
d "k" {
  x = 1
}
'''

FILES["cases/not_dict.hcl"] = '''\
outer {
  a = "str"
}
outer {
  a = { b = 1 }
}
'''

FILES["cases/unicode_ident.hcl"] = '''\
\u00e9t\u00e9 = "summer"
\u03c0 = 3.14159
'''

FILES["cases/whitespace.hcl"] = "   \n\t\n"
FILES["cases/empty.hcl"] = ""
FILES["cases/json_array.hcl"] = '  {"a": [1, 2.5, null, true, "x"], "b": {}}\n'
FILES["cases/json_bad.hcl"] = '{"a": 1,}\n'
FILES["cases/json_dup.hcl"] = '{"a": 1, "b": 2, "a": 3}\n'

# Files the lexer or the parser refuses.
FILES["broken/unterminated_string.hcl"] = 'a = "open\nb = 2\n'
FILES["broken/unterminated_interp.hcl"] = 'a = "${foo(\n'
FILES["broken/unterminated_heredoc.hcl"] = 'a = <<EOF\nno end\n'
FILES["broken/unterminated_comment.hcl"] = 'a = 1\n/* never closed\n'
FILES["broken/stray_close.hcl"] = 'a = 1 */\n'
FILES["broken/single_slash.hcl"] = 'a = 1 / b\n'
FILES["broken/slash_at_end.hcl"] = 'a = 1\n/'
FILES["broken/heredoc_no_marker.hcl"] = 'a = <<\nEOF\n'
FILES["broken/single_lt.hcl"] = 'a = <b\n'
FILES["broken/illegal_char.hcl"] = 'a = 1\nb = @\n'
FILES["broken/missing_value.hcl"] = 'a =\n'
FILES["broken/missing_brace.hcl"] = 'block {\n  a = 1\n'
FILES["broken/extra_brace.hcl"] = 'a = 1\n}\n'
FILES["broken/double_equals.hcl"] = 'a = = 1\n'
FILES["broken/comma_start.hcl"] = ', a = 1\n'
FILES["broken/list_comment_first.hcl"] = 'a = [ # c\n 1 ]\n'
FILES["broken/newline_in_key.hcl"] = 'resource "a" "b" "c" = 1\n'
FILES["broken/tf012_for.hcl"] = 'a = [for s in var.list : upper(s)]\n'
FILES["broken/tab_in_heredoc_marker.hcl"] = 'a = <<EOF\tX\nEOF\n'

FILES["broken/vault_typo.hcl"] = '''\
path "secret/*" {
  capabilities = ["read"
}
'''


def decoder_fixtures():
    return sorted(os.listdir(os.path.join(HERE, "hcl_fixtures", "decoder")))


def lexer_fixtures():
    return sorted(os.listdir(os.path.join(HERE, "hcl_fixtures", "lexer")))


def jobs():
    j = []
    for name in sorted(n for n in FILES if n.startswith("infra/")):
        j.append(["load", name])
    for name in sorted(n for n in FILES if n.startswith("cases/")):
        j.append(["load", name])
    for name in sorted(n for n in FILES if n.startswith("broken/")):
        j.append(["load", name])
    for name in decoder_fixtures():
        j.append(["load", "fixtures/decoder/" + name])
    # exporting comments puts them in the result, where the grammar takes them
    for name in ("cases/comments.hcl", "cases/lists.hcl", "infra/vault/ci.hcl",
                 "fixtures/decoder/array_comment.hcl", "fixtures/decoder/structure_comment.hcl",
                 "fixtures/decoder/multi_line_comment.hcl", "fixtures/decoder/single_line_comment.hcl"):
        for mode in ("LINE", "MULTILINE", "ALL"):
            j.append(["load", name, mode])
    j.append(["load", "cases/comments.hcl", "EVERYTHING"])
    # the token stream itself
    for name in lexer_fixtures():
        j.append(["tokens", "fixtures/lexer/" + name])
    for name in ("cases/numbers.hcl", "cases/strings.hcl", "cases/heredocs.hcl",
                 "cases/crlf_heredoc.hcl", "cases/expressions.hcl", "broken/unterminated_string.hcl",
                 "broken/single_slash.hcl", "broken/illegal_char.hcl"):
        j.append(["tokens", name])
    j.append(["tokens", "cases/comments.hcl", "ALL"])
    # what the infrastructure repo's tooling reads out of the files
    j.append(["terraform", "infra/terraform"])
    j.append(["vault", "infra/vault/admin.hcl", "read:sys/health", "sudo:sys/rotate",
              "read:auth/token/root", "read:secret/data/payments/stripe",
              "update:secret/data/payments/stripe", "delete:secret/app/config", "read:other/path",
              "list:secret/"])
    j.append(["vault", "infra/vault/ci.hcl", "read:secret/data/ci/deploy-key", "read:secret/data/ci/prod-signing",
              "list:secret/metadata/ci/", "update:auth/token/renew-self", "update:transit/encrypt/ci",
              "update:transit/encrypt/prod", "read:secret/data/cia"])
    j.append(["nomad", "infra/nomad/web.nomad"])
    j.append(["consul", "infra/consul/agent.hcl"])
    return j


if os.path.isdir(DATA):
    shutil.rmtree(DATA)
for name, text in FILES.items():
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
for kind in ("decoder", "lexer"):
    dst = os.path.join(DATA, "fixtures", kind)
    os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(os.path.join(HERE, "hcl_fixtures", kind))):
        shutil.copyfile(os.path.join(HERE, "hcl_fixtures", kind, name), os.path.join(dst, name))
with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for job in jobs():
        f.write("\t".join(job) + "\n")
