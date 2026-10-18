#!/usr/bin/env python3
"""Writes data/ for mini_json: real-world JSON documents (an npm manifest,
GeoJSON, a Kubernetes deployment, an issue-tracker API page, a service
config, a JSON Lines access log), edge cases, broken documents, and
data/jobs.tsv."""
import json
import os

D = "data"


def put(name, text):
    path = os.path.join(D, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


PACKAGE = """{
  "name": "@example/cafe-notes",
  "version": "2.4.1",
  "description": "Notes for café owners \\u2014 menus, stock, shifts",
  "keywords": ["notes", "café", "pos"],
  "author": {"name": "José Álvarez", "email": "jose@example.com", "url": "https:\\/\\/example.com\\/~jose"},
  "license": "MIT",
  "main": "dist/index.js",
  "type": "module",
  "engines": {"node": ">=18.0.0"},
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "test": "vitest run --coverage",
    "lint": "eslint \\"src/**/*.{ts,tsx}\\"",
    "prepublishOnly": "npm run build && npm test"
  },
  "dependencies": {"date-fns": "^3.6.0", "zod": "~3.23.8"},
  "devDependencies": {"typescript": "5.5.4", "vitest": "^2.0.5", "eslint": "^9.9.0"},
  "private": false,
  "publishConfig": null,
  "files": [],
  "workspaces": {}
}
"""

GEO = """{"type":"FeatureCollection","features":[
{"type":"Feature","id":1,"geometry":{"type":"Point","coordinates":[-122.4194,37.7749]},"properties":{"name":"San Francisco","population":808437,"area_km2":121.4,"capital":false}},
{"type":"Feature","id":2,"geometry":{"type":"Point","coordinates":[139.6917,35.6895]},"properties":{"name":"東京","population":13960000,"area_km2":2194.07,"capital":true}},
{"type":"Feature","id":3,"geometry":{"type":"LineString","coordinates":[[2.3522,48.8566],[2.2945,48.8584],[2.3376,48.8606]]},"properties":{"name":"Paris walk","length_m":5.2e3,"tags":["museum","river"]}},
{"type":"Feature","id":4,"geometry":{"type":"Polygon","coordinates":[[[0,0],[0,1E-7],[1.0E-7,1e-7],[1e-07,0],[0,0]]]},"properties":{"name":"tiny square","area_km2":1.0e-14}},
{"type":"Feature","id":5,"geometry":null,"properties":{"name":"Null Island","elevation":-0.0,"note":"0.1 + 0.2 = 0.30000000000000004"}}
],"bbox":[-180.0,-90.0,180.0,90.0]}
"""

K8S = """{
	"apiVersion": "apps/v1",
	"kind": "Deployment",
	"metadata": {
		"name": "cafe-api",
		"namespace": "prod",
		"labels": {"app": "cafe-api", "tier": "backend"},
		"annotations": {"deployment.kubernetes.io/revision": "12"}
	},
	"spec": {
		"replicas": 3,
		"revisionHistoryLimit": 10,
		"selector": {"matchLabels": {"app": "cafe-api"}},
		"strategy": {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": "25%", "maxUnavailable": 0}},
		"template": {
			"metadata": {"labels": {"app": "cafe-api"}},
			"spec": {
				"containers": [
					{
						"name": "api",
						"image": "registry.example.com/cafe-api:2.4.1",
						"ports": [{"containerPort": 8080, "protocol": "TCP"}],
						"env": [
							{"name": "DATABASE_URL", "valueFrom": {"secretKeyRef": {"name": "db", "key": "url"}}},
							{"name": "LOG_LEVEL", "value": "info"}
						],
						"resources": {"limits": {"cpu": "500m", "memory": "256Mi"}, "requests": {"cpu": "100m", "memory": "128Mi"}},
						"readinessProbe": {"httpGet": {"path": "/healthz", "port": 8080}, "initialDelaySeconds": 5, "periodSeconds": 10},
						"securityContext": {"runAsNonRoot": true, "readOnlyRootFilesystem": true, "allowPrivilegeEscalation": false}
					}
				],
				"terminationGracePeriodSeconds": 30,
				"nodeSelector": {}
			}
		}
	},
	"status": {}
}
"""

ISSUES = (
    '[\n'
    '  {"id": 1001, "number": 42, "title": "Crash when menu has \\u00e9 or \\ud83d\\ude80 in it", "state": "open",'
    ' "labels": [{"name": "bug", "color": "d73a4a"}, {"name": "unicode", "color": "0e8a16"}],'
    ' "user": {"login": "ana", "site_admin": false}, "comments": 3, "body": "Steps:\\r\\n1. Add \\"Crème brûlée\\"\\n2. Save\\n\\nExpected: <b>saved</b>\\tActual: \\\\crash\\\\",'
    ' "reactions": {"+1": 4, "-1": 0, "heart": 1}, "closed_at": null, "score": 0.8754},\n'
    '  {"id": 1002, "number": 43, "title": "Zero\\u200bwidth space and NBSP\\u00a0in names", "state": "closed",'
    ' "labels": [], "user": {"login": "bo\\u00f8", "site_admin": true}, "comments": 0,'
    ' "body": "Line separator \\u2028 and BOM \\ufeff and bell \\u0007 and DEL \\u007f.", "reactions": {}, "closed_at": "2024-03-09T17:42:05Z", "score": 1}\n'
    ']\n'
)

CONFIG = """{
  "service": "billing",
  "port": 8443,
  "port": 9443,
  "limits": {"max_body": 1048576, "timeout_s": 2.5, "retries": 3},
  "ids": [0, -0, 9223372036854775807, -9223372036854775808, 18446744073709551616, 123456789012345678901234567890],
  "floats": [1.0, 1.5e300, 1e400, -1e400, 1e-400, 5e-324, 2.2250738585072014e-308, 0.1, 100.0, 1e16, 1e15, 12345.6789e-3, -0.0, 3.14159265358979323846],
  "special": [NaN, Infinity, -Infinity],
  "deep": {"a": {"b": {"c": {"d": {"e": [[[[["bottom"]]]]]}}}}},
  "empty": {"s": "", "a": [], "o": {}},
  "dupes": {"k": 1, "j": 2, "k": 3},
  "escapes": "quote \\" backslash \\\\ slash \\/ tab \\t newline \\n cr \\r ff \\f bs \\b nul \\u0000 end",
  "astral": "\\ud834\\udd1e music, \\uD83D\\uDE00 grin, raw 🎉 party",
  "lone": ["\\ud800", "\\udfff", "a\\ud83db", "\\ude00\\ud83d"],
  "unicode_keys": {"ключ": "значение", "مفتاح": "قيمة", "🔑": "🚪"}
}
"""

LOG_LINES = [
    '{"ts":"2024-03-09T17:42:05.123Z","method":"GET","path":"/menu","status":200,"bytes":5120,"ms":12.5,"ua":"curl/8.5.0"}',
    '{"ts":"2024-03-09T17:42:06.004Z","method":"POST","path":"/orders","status":201,"bytes":312,"ms":48.25,"ua":"Mozilla/5.0","user":{"id":7,"name":"Zoë"}}',
    '{"ts":"2024-03-09T17:42:07.500Z","method":"GET","path":"/orders/9","status":404,"bytes":0,"ms":3,"ua":null}',
    '  {"ts":"2024-03-09T17:42:08.000Z", "method":"DELETE", "path":"/orders/7", "status":204, "bytes":0, "ms":7.0}  ',
    '{"ts":"2024-03-09T17:42:09.010Z","method":"GET","path":"/search?q=cr%C3%A8me","status":200,"bytes":2048,"ms":101.0,"tags":["slow"]}',
    '{"ts":"2024-03-09T17:42:10.000Z","method":"GET","path":"/menu","status":500,"bytes":91,"ms":250.75,"error":"upstream timed out (110: Connection timed out)"}',
    '{"ts":"2024-03-09T17:42:11.000Z","method":"GET","path":"/menu","status":200,"bytes":5120,"ms":11.0,}',
    '',
    '{"ts":"2024-03-09T17:42:12.000Z","method":"PUT","path":"/menu/3","status":200,"bytes":77,"ms":1.0e1}',
    '[1, 2, 3]',
    '{"ts":"2024-03-09T17:42:13.000Z" "method":"GET"}',
]

BAD = {
    "empty.json": "",
    "spaces.json": "   \n  ",
    "trailing-comma-array.json": "[1, 2, 3,]",
    "trailing-comma-object.json": '{\n  "a": 1,\n  "b": 2,\n}',
    "double-comma.json": "[\n 1,\n  2,,\n]",
    "missing-colon.json": '{"a" 1}',
    "single-quotes.json": "{'a': 1}",
    "unquoted-key.json": '{a: 1}',
    "missing-comma.json": '[1 2]',
    "unterminated-string.json": '{"name": "caf',
    "control-char.json": '{"name": "caf\x01e"}',
    "raw-newline.json": '["one\ntwo"]',
    "bad-escape.json": '"tab\\q"',
    "bad-u-escape.json": '"\\u12"',
    "bad-u-escape2.json": '"\\u12zz"',
    "bad-low-surrogate.json": '"\\ud83d\\uZZZZ"',
    "leading-zero.json": "[01]",
    "trailing-dot.json": "1.",
    "leading-dot.json": ".5",
    "lone-minus.json": "-",
    "plus-sign.json": "+1",
    "hex.json": "0x1F",
    "extra-data.json": '{"a": 1} {"b": 2}',
    "truncated-true.json": "[tru]",
    "missing-value.json": '{"a":}',
    "open-brace.json": "{",
    "open-bracket.json": "[",
    "open-key.json": '{"a"',
    "open-value.json": '{"a":1',
    "open-array.json": "[1,",
    "comment.json": '{"a": 1 // why not\n}',
    "nan-lower.json": "[nan]",
    "bom.json": "\ufeff{\"a\": 1}",
    "huge-int.json": "[" + "9" * 5000 + "]",
    "multiline-error.json": '{\n  "users": [\n    {"name": "ana"},\n    {"name": "bo" "x"}\n  ]\n}',
    "unicode-before-error.json": '{"日本": "東京", "x": ]}',
}


def main():
    put("package.json", PACKAGE)
    put("cities.geojson", GEO)
    put("deployment.json", K8S)
    put("issues.json", ISSUES)
    put("config.json", CONFIG)
    put("access.jsonl", "\n".join(LOG_LINES) + "\n")
    for name, text in BAD.items():
        put("bad/" + name, text)
    put("ok/scalar.json", ' "just a string" ')
    put("ok/number.json", "-12.5e+2")
    put("ok/null.json", "null")
    put("ok/big-but-legal.json", "[" + "7" * 4300 + "]")

    docs = ["package.json", "cities.geojson", "deployment.json", "issues.json", "config.json",
            "ok/scalar.json", "ok/number.json", "ok/null.json"]
    jobs = []
    for d in docs:
        jobs.append(["load", d])
        jobs.append(["dump", d])
    for d in ["package.json", "deployment.json", "cities.geojson"]:
        jobs.append(["dump", d, "indent=2"])
    jobs.append(["dump", "issues.json", "indent=4", "ensure_ascii=0"])
    jobs.append(["dump", "issues.json", "indent=t", "sort_keys=1"])
    jobs.append(["dump", "config.json", "indent=0"])
    jobs.append(["dump", "config.json", "indent=2", "sort_keys=1", "ensure_ascii=0"])
    jobs.append(["dump", "config.json", "compact=1"])
    jobs.append(["dump", "config.json", "allow_nan=0"])
    jobs.append(["dump", "cities.geojson", "compact=1", "sort_keys=1"])
    jobs.append(["dump", "cities.geojson", "allow_nan=0", "indent=1"])
    jobs.append(["dump", "deployment.json", "compact=1", "indent=2"])
    jobs.append(["dump", "ok/scalar.json", "indent=2"])
    jobs.append(["dump", "ok/big-but-legal.json", "compact=1"])
    jobs.append(["jsonl", "access.jsonl"])
    jobs.append(["jsonl", "access.jsonl", "sort_keys=1", "ensure_ascii=0"])
    jobs.append(["roundtrip", "config.json"])
    jobs.append(["roundtrip", "issues.json"])
    jobs.append(["roundtrip", "cities.geojson"])
    for name in BAD:
        jobs.append(["load", "bad/" + name])
    with open(os.path.join(D, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
