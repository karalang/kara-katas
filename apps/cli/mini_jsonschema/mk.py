# Builds data/: five JSON Schemas (draft 2020-12) from real kinds of use, and
# the instance documents they validate, some valid, some not, some not JSON.
import json, os, shutil

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/schemas")
os.makedirs("data/docs")

def schema(name, s):
    open(f"data/schemas/{name}", "w").write(json.dumps(s, indent=2, ensure_ascii=False) + "\n")

def doc(name, text):
    open(f"data/docs/{name}", "w").write(text)

# ---------------------------------------------------------------- orders API
schema("order.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://shop.example/schemas/order.json",
    "title": "Order",
    "type": "object",
    "required": ["id", "customer", "items", "currency"],
    "properties": {
        "id": {"type": "string", "pattern": "^ord_[0-9a-f]{8}$"},
        "customer": {"$ref": "#/$defs/customer"},
        "items": {
            "type": "array",
            "minItems": 1,
            "maxItems": 50,
            "items": {"$ref": "#/$defs/line"},
        },
        "currency": {"enum": ["USD", "EUR", "GBP", "JPY"]},
        "coupon": {"type": "string", "minLength": 4, "maxLength": 12, "pattern": "^[A-Z0-9]+$"},
        "giftWrap": {"type": "boolean"},
        "giftMessage": {"type": "string", "maxLength": 40},
        "shipping": {"$ref": "#/$defs/address"},
        "notes": {"type": ["string", "null"]},
    },
    "dependentRequired": {"giftWrap": ["giftMessage"]},
    "additionalProperties": False,
    "$defs": {
        "customer": {
            "type": "object",
            "required": ["email", "name"],
            "properties": {
                "email": {"type": "string", "format": "email"},
                "name": {"type": "string", "minLength": 1},
                "vip": {"type": "boolean"},
            },
        },
        "line": {
            "type": "object",
            "required": ["sku", "qty", "price"],
            "properties": {
                "sku": {"type": "string", "pattern": "^[A-Z]{3}-\\d{4}$"},
                "qty": {"type": "integer", "minimum": 1, "maximum": 100},
                "price": {"type": "number", "exclusiveMinimum": 0, "multipleOf": 0.01},
                "discount": {"type": "number", "minimum": 0, "exclusiveMaximum": 1},
            },
            "additionalProperties": False,
        },
        "address": {
            "type": "object",
            "required": ["country", "line1"],
            "properties": {
                "country": {"type": "string", "pattern": "^[A-Z]{2}$"},
                "line1": {"type": "string"},
                "postcode": {"type": "string"},
            },
            "if": {"properties": {"country": {"const": "US"}}},
            "then": {
                "required": ["postcode"],
                "properties": {"postcode": {"pattern": "^\\d{5}(-\\d{4})?$"}},
            },
            "else": {"properties": {"postcode": {"maxLength": 10}}},
        },
    },
})

doc("order-ok.json", """{
  "id": "ord_0a1b2c3d",
  "customer": {"email": "ana@example.com", "name": "Ana Lima", "vip": true},
  "items": [
    {"sku": "TEA-0042", "qty": 2, "price": 4.5},
    {"sku": "MUG-1001", "qty": 1, "price": 12.25, "discount": 0.1}
  ],
  "currency": "EUR",
  "shipping": {"country": "PT", "line1": "Rua Augusta 10", "postcode": "1100-053"},
  "notes": null
}
""")

doc("order-us.json", """{
  "id": "ord_ffff0000",
  "customer": {"email": "not-an-email", "name": "Bo"},
  "items": [{"sku": "PEN-0001", "qty": 10, "price": 1.0}],
  "currency": "USD",
  "shipping": {"country": "US", "line1": "1 Main St", "postcode": "02139-4307"},
  "giftWrap": true,
  "giftMessage": "Happy birthday!"
}
""")

doc("order-bad.json", """{
  "id": "ORD-12",
  "customer": {"email": "kim@example.com", "name": ""},
  "items": [
    {"sku": "TEA-42", "qty": 0, "price": 19.99},
    {"sku": "TEA-0042", "qty": 2.5, "price": -3, "discount": 1},
    {"sku": "CUP-0007", "qty": 101, "price": 0.3, "colour": "red"},
    {"qty": 1}
  ],
  "currency": "usd",
  "coupon": "save10",
  "giftWrap": true,
  "shipping": {"country": "US", "line1": "9 Elm St", "postcode": "9021"},
  "notes": 5,
  "trackingId": "1Z999",
  "source": "app"
}
""")

doc("order-empty.json", """{
  "id": "ord_00000000",
  "customer": "ana@example.com",
  "items": [],
  "currency": "EUR",
  "shipping": {"country": "DE", "postcode": "10115 Berlin-Mitte"}
}
""")

doc("order-array.json", """[{"id": "ord_00000001"}]
""")

# ---------------------------------------------------------------- package.json
schema("package.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "package.json (subset)",
    "type": "object",
    "required": ["name", "version"],
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 214,
            "pattern": "^(?:@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$",
        },
        "version": {
            "type": "string",
            "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?$",
        },
        "private": {"type": "boolean"},
        "keywords": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "license": {
            "anyOf": [
                {"type": "string", "enum": ["MIT", "ISC", "Apache-2.0", "BSD-3-Clause", "UNLICENSED"]},
                {"type": "string", "pattern": "^SEE LICEN[CS]E IN "},
                {"type": "object", "required": ["type"], "properties": {"type": {"type": "string"}}},
            ]
        },
        "bin": {
            "oneOf": [
                {"type": "string"},
                {"type": "object", "additionalProperties": {"type": "string"}, "minProperties": 1},
            ]
        },
        "scripts": {"type": "object", "additionalProperties": {"type": "string"}},
        "dependencies": {"$ref": "#/$defs/deps"},
        "devDependencies": {"$ref": "#/$defs/deps"},
        "engines": {
            "type": "object",
            "properties": {"node": {"type": "string"}},
            "maxProperties": 3,
        },
        "files": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    },
    "$defs": {
        "deps": {
            "type": "object",
            "patternProperties": {
                "^(@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$": {"type": "string"}
            },
            "additionalProperties": False,
        }
    },
})

doc("package-ok.json", """{
  "name": "@acme/log-shipper",
  "version": "2.10.0-rc.1+build.7",
  "private": true,
  "keywords": ["logs", "shipper", "vector"],
  "license": "Apache-2.0",
  "bin": {"shipper": "bin/shipper.js"},
  "scripts": {"test": "node --test", "build": "tsc -p ."},
  "dependencies": {"undici": "^6.19.2", "@acme/core": "workspace:*"},
  "engines": {"node": ">=20"},
  "files": ["dist", "bin"]
}
""")

doc("package-bad.json", """{
  "name": "My_Package",
  "version": "1.02.3",
  "keywords": ["http", "client", "http"],
  "license": "GPL",
  "bin": {},
  "scripts": {"test": ["jest"], "lint": "eslint ."},
  "dependencies": {"left-pad": "1.3.0", "Express": "^4", "lodash": 4},
  "engines": {"node": ">=18", "npm": ">=9", "yarn": "1", "pnpm": "8"},
  "files": []
}
""")

doc("package-license.json", """{
  "name": "tiny",
  "version": "0.0.1",
  "license": "SEE LICENSE IN LICENSE.txt",
  "bin": "cli.js",
  "devDependencies": {"typescript": "5.6.2"}
}
""")

doc("package-license2.json", """{
  "name": "tiny-two",
  "version": "1.0.0",
  "license": {"url": "https://example.com/license"},
  "keywords": [1, true, 1.0, "x"]
}
""")

# ---------------------------------------------------------------- k8s Deployment
schema("deployment.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Deployment (apps/v1, subset)",
    "type": "object",
    "required": ["apiVersion", "kind", "metadata", "spec"],
    "properties": {
        "apiVersion": {"const": "apps/v1"},
        "kind": {"const": "Deployment"},
        "metadata": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"$ref": "#/$defs/dnsName"},
                "namespace": {"$ref": "#/$defs/dnsName"},
                "labels": {
                    "type": "object",
                    "propertyNames": {"maxLength": 63, "pattern": "^[a-z0-9A-Z]([-a-z0-9A-Z_./]*[a-z0-9A-Z])?$"},
                    "additionalProperties": {"type": "string", "maxLength": 63},
                },
            },
        },
        "spec": {
            "type": "object",
            "required": ["selector", "template"],
            "properties": {
                "replicas": {"type": "integer", "minimum": 0},
                "selector": {"type": "object", "minProperties": 1},
                "template": {
                    "type": "object",
                    "properties": {
                        "spec": {
                            "type": "object",
                            "required": ["containers"],
                            "properties": {
                                "containers": {
                                    "type": "array",
                                    "minItems": 1,
                                    "items": {"$ref": "#/$defs/container"},
                                    "contains": {"properties": {"name": {"const": "app"}}, "required": ["name"]},
                                    "maxContains": 1,
                                },
                                "restartPolicy": {"enum": ["Always", "OnFailure", "Never"]},
                            },
                        }
                    },
                },
                "strategy": {
                    "type": "object",
                    "properties": {
                        "type": {"enum": ["RollingUpdate", "Recreate"]},
                        "rollingUpdate": {
                            "type": "object",
                            "properties": {
                                "maxSurge": {"$ref": "#/$defs/intOrPercent"},
                                "maxUnavailable": {"$ref": "#/$defs/intOrPercent"},
                            },
                        },
                    },
                    "if": {"properties": {"type": {"const": "Recreate"}}, "required": ["type"]},
                    "then": {"not": {"required": ["rollingUpdate"]}},
                },
            },
        },
    },
    "$defs": {
        "dnsName": {"type": "string", "maxLength": 63, "pattern": "^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"},
        "intOrPercent": {"oneOf": [{"type": "integer", "minimum": 0}, {"type": "string", "pattern": "^\\d+%$"}]},
        "container": {
            "type": "object",
            "required": ["name", "image"],
            "properties": {
                "name": {"$ref": "#/$defs/dnsName"},
                "image": {"type": "string", "minLength": 1},
                "args": {"type": "array", "items": {"type": "string"}},
                "ports": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["containerPort"],
                        "properties": {
                            "containerPort": {"type": "integer", "minimum": 1, "maximum": 65535},
                            "protocol": {"enum": ["TCP", "UDP", "SCTP"]},
                        },
                    },
                },
                "env": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {"name": {"type": "string"}},
                        "oneOf": [{"required": ["value"]}, {"required": ["valueFrom"]}],
                    },
                },
                "resources": {
                    "type": "object",
                    "properties": {
                        "limits": {"$ref": "#/$defs/quantities"},
                        "requests": {"$ref": "#/$defs/quantities"},
                    },
                },
            },
        },
        "quantities": {
            "type": "object",
            "properties": {
                "cpu": {"type": ["string", "number"], "pattern": "^\\d+(\\.\\d+)?m?$"},
                "memory": {"type": "string", "pattern": "^\\d+(Ki|Mi|Gi|K|M|G)?$"},
            },
            "additionalProperties": False,
        },
    },
})

doc("deploy-ok.json", """{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {"name": "checkout", "namespace": "shop", "labels": {"app.kubernetes.io/name": "checkout", "tier": "web"}},
  "spec": {
    "replicas": 3,
    "selector": {"matchLabels": {"app": "checkout"}},
    "strategy": {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": "25%", "maxUnavailable": 0}},
    "template": {
      "spec": {
        "containers": [
          {"name": "app", "image": "registry.example/checkout:1.8.2",
           "ports": [{"containerPort": 8080, "protocol": "TCP"}],
           "env": [{"name": "MODE", "value": "prod"}, {"name": "DB_URL", "valueFrom": {"secretKeyRef": {"name": "db", "key": "url"}}}],
           "resources": {"limits": {"cpu": "500m", "memory": "256Mi"}, "requests": {"cpu": 0.25, "memory": "128Mi"}}},
          {"name": "envoy", "image": "envoyproxy/envoy:v1.31.0", "args": ["-c", "/etc/envoy.yaml"]}
        ]
      }
    }
  }
}
""")

doc("deploy-bad.json", """{
  "apiVersion": "apps/v1beta2",
  "kind": "Deployment",
  "metadata": {"name": "Checkout_API", "labels": {"-bad": "x", "team": 7}},
  "spec": {
    "replicas": -1,
    "selector": {},
    "strategy": {"type": "Recreate", "rollingUpdate": {"maxSurge": "25 percent"}},
    "template": {
      "spec": {
        "restartPolicy": "Sometimes",
        "containers": [
          {"name": "web", "image": "",
           "ports": [{"containerPort": 70000}, {"protocol": "HTTP"}],
           "env": [{"name": "A"}, {"name": "B", "value": "1", "valueFrom": {}}, {"value": "x"}],
           "resources": {"limits": {"cpu": "1.5 cores", "memory": "1Gb", "gpu": 1}}}
        ]
      }
    }
  }
}
""")

doc("deploy-two-apps.json", """{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {"name": "batch"},
  "spec": {
    "selector": {"matchLabels": {"app": "batch"}},
    "strategy": {"rollingUpdate": {"maxSurge": 1.5}},
    "template": {"spec": {"containers": [
      {"name": "app", "image": "batch:1"},
      {"name": "app", "image": "batch:2"}
    ]}}
  }
}
""")

doc("deploy-no-app.json", """{
  "apiVersion": "apps/v1",
  "kind": "StatefulSet",
  "metadata": {"name": "worker", "labels": {"a-label-name-that-is-far-too-long-for-kubernetes-to-accept-at-all": "v"}},
  "spec": {"selector": {"x": 1}, "template": {"spec": {"containers": [{"name": "sidecar", "image": "s:1"}]}}}
}
""")

# ---------------------------------------------------------------- service config
schema("config.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "service config",
    "type": "object",
    "properties": {
        "listen": {
            "type": "array",
            "prefixItems": [
                {"type": "string", "pattern": "^(\\d{1,3}\\.){3}\\d{1,3}$"},
                {"type": "integer", "minimum": 1, "maximum": 65535},
            ],
            "items": False,
        },
        "workers": {"type": "integer", "multipleOf": 2, "minimum": 2},
        "ratio": {"type": "number", "multipleOf": 0.1, "maximum": 1},
        "level": {"enum": ["debug", "info", "warn", "error", 0, None]},
        "tags": {"type": "array", "uniqueItems": True, "maxItems": 4},
        "limits": {
            "type": "object",
            "propertyNames": {"pattern": "^[a-z_]+$", "maxLength": 12},
            "additionalProperties": {"type": "integer", "exclusiveMinimum": 0},
            "minProperties": 1,
        },
        "mode": {"const": {"tls": True, "versions": [1.2, 1.3]}},
        "legacyAuth": False,
        "admins": {
            "type": "array",
            "items": {"type": "string"},
            "contains": {"pattern": "@ops\\.example$"},
            "minContains": 2,
        },
        "token": {"type": "string", "not": {"pattern": "^(changeme|secret|password)$"}},
        "backoff": {"type": "array", "items": {"type": "number"}, "maxItems": 0},
    },
    "patternProperties": {"^x-": {}},
    "additionalProperties": False,
    "minProperties": 1,
})

doc("config-ok.json", """{
  "listen": ["0.0.0.0", 8443],
  "workers": 8,
  "ratio": 0.5,
  "level": null,
  "tags": ["edge", "eu", 3, [1, 2]],
  "limits": {"max_conn": 1000, "burst": 50},
  "mode": {"tls": true, "versions": [1.2, 1.3]},
  "admins": ["ana@ops.example", "bo@dev.example", "cy@ops.example"],
  "token": "s3cr3t-9f8a",
  "backoff": [],
  "x-owner": "platform"
}
""")

doc("config-bad.json", """{
  "listen": ["localhost", 0, "tcp"],
  "workers": 7,
  "ratio": 0.3,
  "level": "trace",
  "tags": ["a", 1, 1.0, true, false],
  "limits": {"maxConnections": 10, "burst": 0, "RPS": 2.5},
  "mode": {"tls": true, "versions": [1.2]},
  "legacyAuth": {"user": "admin"},
  "admins": ["root@example.com", "ana@ops.example"],
  "token": "changeme",
  "backoff": [1, 2.5],
  "debug": true,
  "verbose": 1
}
""")

doc("config-edge.json", """{
  "listen": ["10.0.0.1"],
  "workers": 4.0,
  "ratio": 1.0000001,
  "level": 0.0,
  "tags": [{"a": 1, "b": 2}, {"b": 2, "a": 1}],
  "limits": {},
  "mode": {"versions": [1.2, 1.3], "tls": true},
  "admins": ["a@b.c"],
  "token": "Changeme",
  "x-": 1
}
""")

doc("config-empty.json", "{}\n")

doc("config-strings.json", """{
  "level": "it's \\"quoted\\"",
  "token": "tab\\there\\nnewline",
  "tags": ["caf\\u00e9", "café", "\\u65e5\\u672c", "\\\\back"],
  "unknown key": "x",
  "it's": 1
}
""")

# ---------------------------------------------------------------- GitHub Actions
schema("workflow.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "GitHub Actions workflow (subset)",
    "type": "object",
    "required": ["on", "jobs"],
    "properties": {
        "name": {"type": "string"},
        "on": {
            "oneOf": [
                {"$ref": "#/$defs/event"},
                {"type": "array", "items": {"$ref": "#/$defs/event"}, "minItems": 1},
                {"type": "object", "propertyNames": {"$ref": "#/$defs/event"}, "minProperties": 1},
            ]
        },
        "jobs": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {"^[_a-zA-Z][a-zA-Z0-9_-]*$": {"$ref": "#/$defs/job"}},
            "additionalProperties": False,
        },
    },
    "$defs": {
        "event": {"enum": ["push", "pull_request", "schedule", "workflow_dispatch", "release"]},
        "job": {
            "type": "object",
            "required": ["runs-on", "steps"],
            "properties": {
                "runs-on": {"type": ["string", "array"]},
                "timeout-minutes": {"type": "number", "exclusiveMinimum": 0, "maximum": 360},
                "needs": {"type": ["string", "array"], "items": {"type": "string"}},
                "steps": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/step"}},
            },
        },
        "step": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "uses": {"type": "string", "pattern": "^[\\w.-]+/[\\w.-]+(/[\\w./-]+)?@[\\w.-]+$|^docker://"},
                "run": {"type": "string"},
                "with": {"type": "object"},
            },
            "anyOf": [{"required": ["uses"]}, {"required": ["run"]}],
            "not": {"required": ["uses", "run"]},
            "dependentSchemas": {"with": {"required": ["uses"]}},
        },
    },
})

doc("workflow-ok.json", """{
  "name": "ci",
  "on": {"push": {"branches": ["main"]}, "pull_request": null},
  "jobs": {
    "test": {
      "runs-on": "ubuntu-24.04",
      "timeout-minutes": 30,
      "steps": [
        {"uses": "actions/checkout@v4"},
        {"uses": "actions/setup-node@v4", "with": {"node-version": 20}},
        {"name": "test", "run": "npm test"}
      ]
    },
    "deploy": {"runs-on": ["self-hosted", "linux"], "needs": ["test"], "steps": [{"uses": "docker://alpine:3.20"}]}
  }
}
""")

doc("workflow-bad.json", """{
  "on": ["push", "merge"],
  "jobs": {
    "build": {
      "runs-on": 22.04,
      "timeout-minutes": 0,
      "steps": [
        {"name": "both", "uses": "actions/checkout@v4", "run": "make"},
        {"name": "neither"},
        {"run": "make", "with": {"x": 1}},
        {"uses": "checkout"}
      ]
    },
    "2nd-job": {"runs-on": "ubuntu-latest", "steps": []},
    "lint": {"steps": [{"run": "ruff ."}], "needs": [1]}
  }
}
""")

doc("workflow-on.json", """{"on": "nightly", "jobs": {}}
""")

doc("workflow-on2.json", """{"on": {"push": {}, "cron": "0 0 * * *"}, "jobs": {"a": {"runs-on": "x", "steps": [{"run": "true"}], "timeout-minutes": 361}}}
""")

# ---------------------------------------------------------------- not JSON
doc("broken-comma.json", """{
  "id": "ord_0a1b2c3d",
  "currency": "EUR"
  "items": []
}
""")
doc("broken-trailing.json", """{"name": "x", "version": "1.0.0",}
""")
doc("broken-quote.json", """{'name': 'x'}
""")
doc("broken-string.json", """{"name": "unterminated
}
""")
doc("broken-extra.json", """{"a": 1} {"b": 2}
""")
doc("broken-empty.json", "")
doc("broken-escape.json", """{"path": "C:\\Users\\ana"}
""")
doc("broken-number.json", """{"workers": 012}
""")
doc("broken-colon.json", """{"workers" 4}
""")
doc("broken-literal.json", """{"debug": True}
""")

shutil.copy("jobs.txt", "data/jobs.txt")
