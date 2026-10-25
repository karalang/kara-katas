# Writes data/: the JavaScript sources under data/src/ (a small orders
# service as ES modules, a jQuery plugin and polyfills as scripts, a
# CommonJS command-line tool, some libraries, and short snippets under
# data/src/snip/, one per syntax form or error), and the jobs in
# data/jobs.tsv: id, operation, path under data/src/, script or module,
# and the options.
import os

SOURCES = {
    'app/config.js':
        '// Service configuration, with environment overrides.\n'
        "const env = typeof process !== 'undefined' ? process.env : {};\n"
        '\n'
        'const int = (name, fallback) => {\n'
        '  const raw = env[name];\n'
        "  return raw === undefined || raw === '' ? fallback : parseInt(raw, 10);\n"
        '};\n'
        '\n'
        "const FEATURE_PREFIX = 'FEATURE_';\n"
        '\n'
        'export const config = {\n'
        "  port: int('PORT', 8080),\n"
        '  api: { prefix: \'/api/v1\', version: "1.4.2" },\n'
        '  db: {\n'
        "    url: env.DB_URL || 'mem://orders',\n"
        "    latency: int('DB_LATENCY_MS', 0),\n"
        '    maxDocs: 5e4,\n'
        '  },\n'
        '  limits: {\n'
        '    body: 0x100000,\n'
        "    'requests-per-minute': 600,\n"
        '    timeoutMs: 30 * 1000,\n'
        '  },\n'
        '  features: Object.keys(env)\n'
        '    .filter((k) => k.indexOf(FEATURE_PREFIX) === 0)\n'
        "    .reduce((acc, k) => ({ ...acc, [k.slice(FEATURE_PREFIX.length).toLowerCase()]: env[k] === '1' }), {}),\n"
        '  get production() {\n'
        "    return env.NODE_ENV === 'production';\n"
        '  },\n'
        '  describe() {\n'
        "    return `port ${this.port}, db ${this.db.url}${this.production ? ' (production)' : ''}`;\n"
        '  },\n'
        '};\n'
        '\n'
        'export const tiers = [\n'
        "  { name: 'free', rate: 0, quota: 1e3 },\n"
        "  { name: 'team', rate: 12.5, quota: 25e3 },\n"
        "  { name: 'business', rate: 49.99, quota: 1e6 },\n"
        '];\n',
    'app/db.js':
        '/* In-memory document store with the same interface as the real driver.\n'
        ' * Every operation is async so callers do not change when it is swapped. */\n'
        "import { deepClone, sleep } from './util.js';\n"
        '\n'
        'const DEFAULTS = { latency: 0, maxDocs: 10000 };\n'
        '\n'
        'export default class Database {\n'
        '  constructor(options) {\n'
        '    this.options = Object.assign({}, DEFAULTS, options);\n'
        '    this.tables = new Map();\n'
        '    this.nextId = 1;\n'
        '  }\n'
        '\n'
        '  table(name) {\n'
        '    let t = this.tables.get(name);\n'
        '    if (t === undefined) {\n'
        '      t = new Map();\n'
        '      this.tables.set(name, t);\n'
        '    }\n'
        '    return t;\n'
        '  }\n'
        '\n'
        '  async find(name, id) {\n'
        '    await sleep(this.options.latency);\n'
        '    const doc = this.table(name).get(id);\n'
        '    return doc ? deepClone(doc) : null;\n'
        '  }\n'
        '\n'
        '  async insert(name, doc) {\n'
        '    const t = this.table(name);\n'
        '    if (t.size >= this.options.maxDocs) {\n'
        '      throw new Error(`table ${name} is full (${this.options.maxDocs} documents)`);\n'
        '    }\n'
        '    const id = this.nextId++;\n'
        '    t.set(id, Object.freeze({ ...deepClone(doc), id }));\n'
        '    return id;\n'
        '  }\n'
        '\n'
        '  async remove(name, id) {\n'
        '    return this.table(name).delete(id);\n'
        '  }\n'
        '\n'
        '  *scan(name, predicate = () => true) {\n'
        '    for (const [id, doc] of this.table(name)) {\n'
        '      if (predicate(doc, id)) {\n'
        '        yield doc;\n'
        '      }\n'
        '    }\n'
        '  }\n'
        '\n'
        '  async count(name, predicate) {\n'
        '    let n = 0;\n'
        '    for (const _ of this.scan(name, predicate)) n += 1;\n'
        '    return n;\n'
        '  }\n'
        '}\n'
        '\n'
        'export async function connect({ url, latency = 0, ...rest }) {\n'
        '  if (!/^mem:\\/\\/[a-z][\\w-]*$/i.test(url)) {\n'
        "    throw new TypeError('expected a mem:// url, got ' + JSON.stringify(url));\n"
        '  }\n'
        '  const db = new Database({ latency, ...rest });\n'
        '  db.url = url;\n'
        '  return db;\n'
        '}\n',
    'app/router.js':
        '// A small router: routes are a method, a string or a regular expression,\n'
        '// and an async handler.\n'
        "import { escapeRegExp } from './util.js';\n"
        '\n'
        'export class NotFound extends Error {\n'
        '  constructor(what) {\n'
        '    super(`not found: ${what}`);\n'
        "    this.name = 'NotFound';\n"
        '  }\n'
        '}\n'
        '\n'
        "const METHODS = ['get', 'post', 'put', 'delete', 'patch'];\n"
        '\n'
        'export class Router {\n'
        "  constructor({ prefix = '', strict = false } = {}) {\n"
        '    this.prefix = prefix;\n'
        '    this.strict = strict;\n'
        '    this.routes = [];\n'
        '    this._hits = 0;\n'
        '  }\n'
        '\n'
        '  static compile(path) {\n'
        '    if (path instanceof RegExp) {\n'
        '      return path;\n'
        '    }\n'
        '    const source = path\n'
        "      .split('/')\n"
        "      .map((part) => (part.startsWith(':') ? '([^/]+)' : escapeRegExp(part)))\n"
        "      .join('\\\\/');\n"
        "    return new RegExp('^' + source + '$');\n"
        '  }\n'
        '\n'
        '  get size() {\n'
        '    return this.routes.length;\n'
        '  }\n'
        '\n'
        '  get hits() {\n'
        '    return this._hits;\n'
        '  }\n'
        '\n'
        '  set hits(value) {\n'
        "    if (value < 0) throw new RangeError('hits must not be negative');\n"
        '    this._hits = value;\n'
        '  }\n'
        '\n'
        '  add(method, path, handler) {\n'
        '    this.routes.push({ method: method.toUpperCase(), pattern: Router.compile(path), handler });\n'
        '    return this;\n'
        '  }\n'
        '\n'
        '  *match(method, url) {\n'
        '    const path = url.startsWith(this.prefix) ? url.slice(this.prefix.length) : url;\n'
        '    for (const route of this.routes) {\n'
        '      if (route.method !== method) continue;\n'
        "      const m = route.pattern.exec(this.strict ? path : path.replace(/\\/+$/, ''));\n"
        '      if (m !== null) yield [route, m.slice(1)];\n'
        '    }\n'
        '  }\n'
        '\n'
        '  async dispatch(req, res) {\n'
        '    this.hits++;\n'
        '    for (const [route, params] of this.match(req.method, req.url)) {\n'
        '      const result = await route.handler(req, res, params);\n'
        '      if (result !== undefined) return result;\n'
        '    }\n'
        '    throw new NotFound(req.url);\n'
        '  }\n'
        '}\n'
        '\n'
        'for (const method of METHODS) {\n'
        '  Router.prototype[method] = function (path, handler) {\n'
        '    return this.add(method, path, handler);\n'
        '  };\n'
        '}\n',
    'app/server.js':
        '// HTTP entry point for the orders service.\n'
        "import http from 'node:http';\n"
        "import { Router, NotFound } from './router.js';\n"
        "import Database, { connect as openDb } from './db.js';\n"
        "import * as util from './util.js';\n"
        "import { config } from './config.js';\n"
        '\n'
        'const router = new Router({ prefix: config.api.prefix });\n'
        'let db = null;\n'
        '\n'
        '/**\n'
        ' * Reads the whole request body as text.\n'
        ' */\n'
        'function readBody(req, limit = config.limits.body) {\n'
        '  return new Promise((resolve, reject) => {\n'
        '    const chunks = [];\n'
        '    let size = 0;\n'
        "    req.on('data', (chunk) => {\n"
        '      size += chunk.length;\n'
        '      if (size > limit) {\n'
        '        reject(new Error(`body larger than ${util.formatBytes(limit)}`));\n'
        '        req.destroy();\n'
        '        return;\n'
        '      }\n'
        '      chunks.push(chunk);\n'
        '    });\n'
        "    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));\n"
        "    req.on('error', reject);\n"
        '  });\n'
        '}\n'
        '\n'
        'router.get(/^\\/orders\\/(\\d+)$/, async (req, res, [id]) => {\n'
        "  const order = await db.find('orders', Number(id));\n"
        '  if (!order) {\n'
        '    throw new NotFound(`order ${id}`);\n'
        '  }\n'
        '  return { status: 200, body: order };\n'
        '});\n'
        '\n'
        "router.post('/orders', async (req, res) => {\n"
        '  const text = await readBody(req);\n'
        '  let input;\n'
        '  try {\n'
        '    input = JSON.parse(text);\n'
        '  } catch (err) {\n'
        "    return { status: 400, body: { error: 'invalid JSON', detail: err.message } };\n"
        '  }\n'
        '  const { customer, items = [], ...rest } = input;\n'
        "  if (typeof customer !== 'string' || items.length === 0) {\n"
        "    return { status: 422, body: { error: 'customer and items are required' } };\n"
        '  }\n'
        '  const total = items.reduce((sum, { price, qty = 1 }) => sum + price * qty, 0);\n'
        "  const id = await db.insert('orders', { customer, items, total, ...rest, created: Date.now() });\n"
        '  return { status: 201, body: { id, total: util.round(total, 2) } };\n'
        '});\n'
        '\n'
        'router.delete(/^\\/orders\\/(\\d+)$/, async (req, res, [id]) => {\n'
        "  const removed = await db.remove('orders', +id);\n"
        "  return removed ? { status: 204 } : { status: 404, body: { error: 'no such order' } };\n"
        '});\n'
        '\n'
        'const log = util.debounce((line) => console.log(line), 50);\n'
        '\n'
        'async function handle(req, res) {\n'
        '  const started = process.hrtime.bigint ? process.hrtime() : [0, 0];\n'
        '  let result;\n'
        '  try {\n'
        '    result = await router.dispatch(req, res);\n'
        '  } catch (err) {\n'
        '    result = err instanceof NotFound\n'
        '      ? { status: 404, body: { error: err.message } }\n'
        "      : { status: 500, body: { error: 'internal error' } };\n"
        '  } finally {\n'
        '    const [s, ns] = process.hrtime(started);\n'
        '    log(`${req.method} ${req.url} ${result && result.status} ${(s * 1e3 + ns / 1e6).toFixed(1)}ms`);\n'
        '  }\n'
        "  res.writeHead(result.status, { 'content-type': 'application/json' });\n"
        "  res.end(result.body === undefined ? '' : JSON.stringify(result.body));\n"
        '}\n'
        '\n'
        'export async function start(port = config.port) {\n'
        '  db = await openDb(config.db);\n'
        '  const server = http.createServer(handle);\n'
        '  await new Promise((resolve) => server.listen(port, resolve));\n'
        '  return server;\n'
        '}\n'
        '\n'
        'export default start;\n',
    'app/util.js':
        '// Helpers shared by the service.\n'
        '\n'
        'export const KB = 1 << 10;\n'
        'export const MB = KB * KB;\n'
        "const UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB'];\n"
        '\n'
        'export function debounce(fn, wait = 100) {\n'
        '  let timer = null;\n'
        '  return function (...args) {\n'
        '    clearTimeout(timer);\n'
        '    timer = setTimeout(() => fn.apply(this, args), wait);\n'
        '  };\n'
        '}\n'
        '\n'
        'export function throttle(fn, interval) {\n'
        '  let last = -Infinity, pending = null;\n'
        '  return (...args) => {\n'
        '    const now = Date.now();\n'
        '    if (now - last >= interval) {\n'
        '      last = now;\n'
        '      fn(...args);\n'
        '    } else {\n'
        '      pending = args;\n'
        '    }\n'
        '  };\n'
        '}\n'
        '\n'
        'export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
        '\n'
        'export function round(x, digits = 0) {\n'
        '  const f = 10 ** digits;\n'
        '  return Math.round(x * f) / f;\n'
        '}\n'
        '\n'
        'function formatBytes(n) {\n'
        '  let i = 0;\n'
        '  while (n >= 1024 && i < UNITS.length - 1) {\n'
        '    n /= 1024;\n'
        '    i++;\n'
        '  }\n'
        '  return `${i === 0 ? n : n.toFixed(1)} ${UNITS[i]}`;\n'
        '}\n'
        '\n'
        'function deepClone(value, seen = new WeakMap()) {\n'
        "  if (value === null || typeof value !== 'object') return value;\n"
        '  if (seen.has(value)) return seen.get(value);\n'
        '  if (value instanceof Date) return new Date(value.getTime());\n'
        '  const copy = Array.isArray(value) ? [] : {};\n'
        '  seen.set(value, copy);\n'
        '  for (const key of Object.keys(value)) {\n'
        '    copy[key] = deepClone(value[key], seen);\n'
        '  }\n'
        '  return copy;\n'
        '}\n'
        '\n'
        "const group = (n) => String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');\n"
        '\n'
        'export function escapeRegExp(s) {\n'
        "  return s.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');\n"
        '}\n'
        '\n'
        'export function hash32(text) {\n'
        '  let h = 0x811c9dc5;\n'
        '  for (let i = 0; i < text.length; i++) {\n'
        '    h ^= text.charCodeAt(i);\n'
        '    h = (h * 0x01000193) >>> 0;\n'
        '  }\n'
        "  return h.toString(16).padStart(8, '0');\n"
        '}\n'
        '\n'
        'export { formatBytes, deepClone, group as groupDigits };\n',
    'legacy/polyfill.js':
        '// Polyfills for the browsers in the support matrix that lack them.\n'
        'if (!Array.prototype.includes) {\n'
        "  Object.defineProperty(Array.prototype, 'includes', {\n"
        '    value: function (search, fromIndex) {\n'
        '      if (this == null) {\n'
        '        throw new TypeError(\'"this" is null or not defined\');\n'
        '      }\n'
        '      var o = Object(this);\n'
        '      var len = o.length >>> 0;\n'
        '      if (len === 0) {\n'
        '        return false;\n'
        '      }\n'
        '      var n = fromIndex | 0;\n'
        '      var k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);\n'
        '      function sameValueZero(x, y) {\n'
        "        return x === y || (typeof x === 'number' && typeof y === 'number' && isNaN(x) && isNaN(y));\n"
        '      }\n'
        '      while (k < len) {\n'
        '        if (sameValueZero(o[k], search)) {\n'
        '          return true;\n'
        '        }\n'
        '        k++;\n'
        '      }\n'
        '      return false;\n'
        '    }\n'
        '  });\n'
        '}\n'
        '\n'
        "if (typeof Object.assign !== 'function') {\n"
        '  Object.assign = function assign(target) {\n'
        '    if (target == null) {\n'
        "      throw new TypeError('Cannot convert undefined or null to object');\n"
        '    }\n'
        '    var to = Object(target);\n'
        '    for (var index = 1; index < arguments.length; index++) {\n'
        '      var source = arguments[index];\n'
        '      if (source != null) {\n'
        '        for (var key in source) {\n'
        '          if (Object.prototype.hasOwnProperty.call(source, key)) {\n'
        '            to[key] = source[key];\n'
        '          }\n'
        '        }\n'
        '      }\n'
        '    }\n'
        '    return to;\n'
        '  };\n'
        '}\n'
        '\n'
        'if (!String.prototype.padStart) {\n'
        '  String.prototype.padStart = function padStart(targetLength, padString) {\n'
        '    targetLength = targetLength >> 0;\n'
        "    padString = String(typeof padString !== 'undefined' ? padString : ' ');\n"
        '    if (this.length >= targetLength) {\n'
        '      return String(this);\n'
        '    }\n'
        '    targetLength = targetLength - this.length;\n'
        '    if (targetLength > padString.length) {\n'
        '      padString += padString.repeat(targetLength / padString.length);\n'
        '    }\n'
        '    return padString.slice(0, targetLength) + String(this);\n'
        '  };\n'
        '}\n'
        '\n'
        '(function () {\n'
        "  var lastTime = 0, vendors = ['ms', 'moz', 'webkit', 'o'];\n"
        '  for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {\n'
        "    window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];\n"
        '  }\n'
        '  if (!window.requestAnimationFrame) {\n'
        '    window.requestAnimationFrame = function (callback) {\n'
        '      var currTime = new Date().getTime();\n'
        '      var timeToCall = Math.max(0, 16 - (currTime - lastTime));\n'
        '      var id = window.setTimeout(function () { callback(currTime + timeToCall); }, timeToCall);\n'
        '      lastTime = currTime + timeToCall;\n'
        '      return id;\n'
        '    };\n'
        '  }\n'
        '  do {\n'
        '    lastTime--;\n'
        '  } while (lastTime > 0 && false);\n'
        '}());\n',
    'legacy/tabs.js':
        '/*!\n'
        ' * Tabs plugin v2.3.1, the jQuery version the admin pages still load.\n'
        ' */\n'
        ';(function ($, window, document, undefined) {\n'
        "  'use strict';\n"
        '\n'
        "  var pluginName = 'tabs',\n"
        '      defaults = {\n'
        '        active: 0,\n'
        "        activeClass: 'is-active',\n"
        '        animate: true,\n'
        '        duration: 200\n'
        '      };\n'
        '\n'
        '  function Plugin(element, options) {\n'
        '    this.element = element;\n'
        '    this.settings = $.extend({}, defaults, options);\n'
        '    this._defaults = defaults;\n'
        '    this._name = pluginName;\n'
        '    this.init();\n'
        '  }\n'
        '\n'
        '  $.extend(Plugin.prototype, {\n'
        '    init: function () {\n'
        '      var self = this, $el = $(this.element);\n'
        '      this.$tabs = $el.find(\'[role="tab"]\');\n'
        '      this.$panels = $el.find(\'[role="tabpanel"]\');\n'
        "      this.$tabs.on('click.' + pluginName, function (e) {\n"
        '        e.preventDefault();\n'
        '        self.show(self.$tabs.index(this));\n'
        '      });\n'
        "      $el.on('keydown.' + pluginName, function (e) {\n"
        '        switch (e.which) {\n'
        '          case 37: // left\n'
        '          case 38: // up\n'
        '            self.show(self.current - 1);\n'
        '            break;\n'
        '          case 39:\n'
        '          case 40:\n'
        '            self.show(self.current + 1);\n'
        '            break;\n'
        '          case 36:\n'
        '            self.show(0);\n'
        '            break;\n'
        '          case 35:\n'
        '            self.show(self.$tabs.length - 1);\n'
        '            break;\n'
        '          default:\n'
        '            return;\n'
        '        }\n'
        '        e.preventDefault();\n'
        '      });\n'
        '      this.show(this.settings.active, true);\n'
        '    },\n'
        '\n'
        '    show: function (index, instant) {\n'
        '      var n = this.$tabs.length;\n'
        '      if (n === 0) return;\n'
        '      index = ((index % n) + n) % n;\n'
        "      this.$tabs.removeClass(this.settings.activeClass).attr('aria-selected', 'false');\n"
        "      this.$tabs.eq(index).addClass(this.settings.activeClass).attr('aria-selected', 'true');\n"
        '      this.$panels.hide();\n'
        '      if (this.settings.animate && !instant) {\n'
        '        this.$panels.eq(index).fadeIn(this.settings.duration);\n'
        '      } else {\n'
        '        this.$panels.eq(index).show();\n'
        '      }\n'
        '      this.current = index;\n'
        "      $(this.element).trigger('shown.' + pluginName, [index]);\n"
        '    },\n'
        '\n'
        '    destroy: function () {\n'
        "      this.$tabs.off('.' + pluginName);\n"
        "      $(this.element).off('.' + pluginName).removeData('plugin_' + pluginName);\n"
        '    }\n'
        '  });\n'
        '\n'
        '  $.fn[pluginName] = function (options) {\n'
        '    var args = Array.prototype.slice.call(arguments, 1);\n'
        '    return this.each(function () {\n'
        "      var instance = $.data(this, 'plugin_' + pluginName);\n"
        '      if (!instance) {\n'
        "        $.data(this, 'plugin_' + pluginName, new Plugin(this, options));\n"
        "      } else if (typeof options === 'string' && options.charAt(0) !== '_' && typeof instance[options] === 'function') {\n"
        '        instance[options].apply(instance, args);\n'
        '      }\n'
        '    });\n'
        '  };\n'
        '})(jQuery, window, document);\n',
    'lib/csv.js':
        '// RFC 4180 CSV reader as a character state machine.\n'
        'var FIELD_START = 0, UNQUOTED = 1, QUOTED = 2, QUOTE_IN_QUOTED = 3;\n'
        '\n'
        'function parseCSV(text, delimiter) {\n'
        "  delimiter = delimiter || ',';\n"
        "  var rows = [], row = [], field = '', state = FIELD_START;\n"
        '  var i, c;\n'
        '  for (i = 0; i < text.length; i += 1) {\n'
        '    c = text.charAt(i);\n'
        '    switch (state) {\n'
        '      case FIELD_START:\n'
        '        if (c === \'"\') { state = QUOTED; break; }\n'
        '        state = UNQUOTED;\n'
        '        /* falls through */\n'
        '      case UNQUOTED:\n'
        '        if (c === delimiter) {\n'
        "          row.push(field); field = ''; state = FIELD_START;\n"
        "        } else if (c === '\\n' || c === '\\r') {\n"
        "          if (c === '\\r' && text.charAt(i + 1) === '\\n') i++;\n"
        '          row.push(field); rows.push(row);\n'
        "          row = []; field = ''; state = FIELD_START;\n"
        '        } else {\n'
        '          field += c;\n'
        '        }\n'
        '        break;\n'
        '      case QUOTED:\n'
        '        if (c === \'"\') state = QUOTE_IN_QUOTED;\n'
        '        else field += c;\n'
        '        break;\n'
        '      case QUOTE_IN_QUOTED:\n'
        '        if (c === \'"\') { field += \'"\'; state = QUOTED; }\n'
        "        else if (c === delimiter) { row.push(field); field = ''; state = FIELD_START; }\n"
        "        else if (c === '\\n') { row.push(field); rows.push(row); row = []; field = ''; state = FIELD_START; }\n"
        "        else throw new SyntaxError('unexpected ' + JSON.stringify(c) + ' after closing quote at ' + i);\n"
        '        break;\n'
        '    }\n'
        '  }\n'
        "  if (state === QUOTED) throw new SyntaxError('unterminated quoted field');\n"
        "  if (field !== '' || row.length > 0) { row.push(field); rows.push(row); }\n"
        '  return rows;\n'
        '}\n'
        '\n'
        'function toObjects(rows) {\n'
        '  var header = rows[0], out = [], r, o, j;\n'
        '  for (r = 1; r < rows.length; r++) {\n'
        '    o = {};\n'
        '    for (j = 0; j < header.length; j++) o[header[j]] = j < rows[r].length ? rows[r][j] : null;\n'
        '    out[out.length] = o;\n'
        '  }\n'
        '  return out;\n'
        '}\n'
        '\n'
        'var SAMPLE = \'name,city,note\\n"Okafor, J.",Lagos,"said ""hi"""\\r\\nUeda,Kyoto,\\tтест\\u00e9\\n\';\n'
        '\n'
        "if (typeof module !== 'undefined') module.exports = { parseCSV: parseCSV, toObjects: toObjects, SAMPLE: SAMPLE };\n",
    'lib/events.js':
        '// A typed event emitter with once(), off() and async waiting.\n'
        'export class Emitter {\n'
        '  constructor() {\n'
        '    this.listeners = new Map();\n'
        '  }\n'
        '\n'
        '  on(event, fn, { once = false, prepend = false } = {}) {\n'
        '    const list = this.listeners.get(event) || [];\n'
        '    const entry = { fn, once };\n'
        '    prepend ? list.unshift(entry) : list.push(entry);\n'
        '    this.listeners.set(event, list);\n'
        '    return () => this.off(event, fn);\n'
        '  }\n'
        '\n'
        '  once(event, fn) {\n'
        '    return this.on(event, fn, { once: true });\n'
        '  }\n'
        '\n'
        '  off(event, fn) {\n'
        '    const list = this.listeners.get(event);\n'
        '    if (!list) return false;\n'
        '    const i = list.findIndex((e) => e.fn === fn);\n'
        '    if (i < 0) return false;\n'
        '    list.splice(i, 1);\n'
        '    if (list.length === 0) this.listeners.delete(event);\n'
        '    return true;\n'
        '  }\n'
        '\n'
        '  emit(event, ...args) {\n'
        '    const list = this.listeners.get(event);\n'
        '    if (!list) {\n'
        "      if (event === 'error') throw args[0] instanceof Error ? args[0] : new Error(String(args[0]));\n"
        '      return false;\n'
        '    }\n'
        '    for (const entry of [...list]) {\n'
        '      if (entry.once) this.off(event, entry.fn);\n'
        '      entry.fn.apply(this, args);\n'
        '    }\n'
        '    return true;\n'
        '  }\n'
        '\n'
        '  wait(event, timeoutMs = 0) {\n'
        '    return new Promise((resolve, reject) => {\n'
        '      let timer;\n'
        '      const done = this.once(event, (...args) => {\n'
        '        clearTimeout(timer);\n'
        '        resolve(args.length <= 1 ? args[0] : args);\n'
        '      });\n'
        '      if (timeoutMs > 0) {\n'
        '        timer = setTimeout(() => {\n'
        '          done();\n'
        '          reject(new Error(`timed out waiting for ${event} after ${timeoutMs}ms`));\n'
        '        }, timeoutMs);\n'
        '      }\n'
        '    });\n'
        '  }\n'
        '\n'
        '  static mixin(target) {\n'
        '    const e = new Emitter();\n'
        "    for (const name of ['on', 'once', 'off', 'emit', 'wait']) {\n"
        '      target[name] = e[name].bind(e);\n'
        '    }\n'
        '    return target;\n'
        '  }\n'
        '}\n'
        '\n'
        'export const bus = new Emitter();\n',
    'lib/iter.js':
        '// Iteration helpers: lazy sequences built on generators.\n'
        'function* range(start, stop, step = 1) {\n'
        '  if (stop === undefined) {\n'
        '    [start, stop] = [0, start];\n'
        '  }\n'
        '  for (let i = start; step > 0 ? i < stop : i > stop; i += step) yield i;\n'
        '}\n'
        '\n'
        'function* take(n, iterable) {\n'
        '  if (n <= 0) return;\n'
        '  for (const x of iterable) {\n'
        '    yield x;\n'
        '    if (--n === 0) return;\n'
        '  }\n'
        '}\n'
        '\n'
        'function* chunk(iterable, size) {\n'
        '  let buf = [];\n'
        '  for (const x of iterable) {\n'
        '    buf.push(x);\n'
        '    if (buf.length === size) {\n'
        '      yield buf;\n'
        '      buf = [];\n'
        '    }\n'
        '  }\n'
        '  if (buf.length) yield buf;\n'
        '}\n'
        '\n'
        'function* flatten(iterable, depth = Infinity) {\n'
        '  for (const x of iterable) {\n'
        "    if (depth > 0 && x != null && typeof x[Symbol.iterator] === 'function' && typeof x !== 'string') {\n"
        '      yield* flatten(x, depth - 1);\n'
        '    } else {\n'
        '      yield x;\n'
        '    }\n'
        '  }\n'
        '}\n'
        '\n'
        'const zip = (...its) => ({\n'
        '  *[Symbol.iterator]() {\n'
        '    const iters = its.map((it) => it[Symbol.iterator]());\n'
        '    while (true) {\n'
        '      const steps = iters.map((it) => it.next());\n'
        '      if (steps.some((s) => s.done)) return;\n'
        '      yield steps.map((s) => s.value);\n'
        '    }\n'
        '  },\n'
        '});\n'
        '\n'
        'function find2d(grid, target) {\n'
        '  let found = null;\n'
        '  search: for (let r = 0; r < grid.length; r++) {\n'
        '    for (let c = 0; c < grid[r].length; c++) {\n'
        '      if (grid[r][c] === target) {\n'
        '        found = { r, c };\n'
        '        break search;\n'
        '      }\n'
        '      if (grid[r][c] > target) continue search;\n'
        '    }\n'
        '  }\n'
        '  return found;\n'
        '}\n'
        '\n'
        'const html = (strings, ...values) =>\n'
        '  strings.reduce((out, s, i) => out + s + (i < values.length ? String(values[i]).replace(/[&<>"]/g, (ch) => `&#${ch.charCodeAt(0)};`) : \'\'), \'\');\n'
        '\n'
        "const row = (cells) => html`<tr>${cells.map((c) => `<td>${c}</td>`).join('')}</tr>`;\n"
        '\n'
        'const sum = async (promises) => (await Promise.all(promises)).reduce((a, b) => a + b, 0);\n'
        'const square = async x => x ** 2;\n'
        'let total = 0;\n'
        'total **= 2;\n'
        "total = void 0, total = typeof total === 'undefined' ? 0 : total;\n"
        '\n'
        'function Point(x, y) {\n'
        '  if (!new.target) return new Point(x, y);\n'
        '  this.x = x;\n'
        '  this.y = y;\n'
        '}\n'
        '\n'
        'const base = {\n'
        "  greet() { return 'hello'; },\n"
        '};\n'
        'const derived = {\n'
        '  __proto__: base,\n'
        "  greet() { return super.greet() + ', world'; },\n"
        '};\n',
    'lib/queue.js':
        '// A job queue with bounded concurrency and retries (uses class fields).\n'
        "import { Emitter } from './events.js';\n"
        '\n'
        'export class Queue extends Emitter {\n'
        '  static defaults = { concurrency: 4, retries: 2, backoffMs: 250 };\n'
        '  running = 0;\n'
        '  done = 0;\n'
        '  failed = 0;\n'
        '  pending = [];\n'
        '\n'
        '  constructor(options = {}) {\n'
        '    super();\n'
        '    this.options = { ...Queue.defaults, ...options };\n'
        '  }\n'
        '\n'
        '  push(task, meta = {}) {\n'
        '    this.pending.push({ task, meta, attempt: 0 });\n'
        "    this.emit('queued', meta);\n"
        '    this.tick();\n'
        '    return this;\n'
        '  }\n'
        '\n'
        '  tick() {\n'
        '    while (this.running < this.options.concurrency && this.pending.length > 0) {\n'
        '      this.run(this.pending.shift());\n'
        '    }\n'
        "    if (this.running === 0 && this.pending.length === 0) this.emit('drain', { done: this.done, failed: this.failed });\n"
        '  }\n'
        '\n'
        '  async run(job) {\n'
        '    this.running++;\n'
        '    try {\n'
        '      const value = await job.task(job.meta);\n'
        '      this.done++;\n'
        "      this.emit('done', job.meta, value);\n"
        '    } catch (err) {\n'
        '      if (job.attempt < this.options.retries) {\n'
        '        job.attempt += 1;\n'
        '        const delay = this.options.backoffMs * 2 ** (job.attempt - 1);\n'
        '        setTimeout(() => {\n'
        '          this.pending.unshift(job);\n'
        '          this.tick();\n'
        '        }, delay);\n'
        '      } else {\n'
        '        this.failed++;\n'
        "        this.emit('failed', job.meta, err);\n"
        '      }\n'
        '    } finally {\n'
        '      this.running--;\n'
        '      this.tick();\n'
        '    }\n'
        '  }\n'
        '\n'
        '  get size() {\n'
        '    return this.pending.length + this.running;\n'
        '  }\n'
        '}\n',
    'lib/units.js':
        '// Unit conversion tables. Sloppy-mode script: it still has a legacy\n'
        '// octal permission mask and an octal escape from the original author.\n'
        'var MODE_DEFAULT = 0644, MODE_EXEC = 0o755, MASK = 0b111111111;\n'
        'var LIMITS = {\n'
        '  maxSafe: 9007199254740991,\n'
        '  beyondSafe: 9007199254740993,\n'
        '  googol: 1e100,\n'
        '  huge: 0xFFFFFFFFFFFFFFFFFFFF,\n'
        '  tooBig: 1e400,\n'
        '  tiny: 5e-324,\n'
        '  epsilon: 2.220446049250313e-16,\n'
        '  third: 1 / 3,\n'
        '  half: .5,\n'
        '  whole: 5.,\n'
        '  sci: 6.02214076e23,\n'
        '  grams: 1.5e-7,\n'
        '  digits: 123456789012345678901234567890\n'
        '};\n'
        '\n'
        'var LENGTH = { mm: 0.001, cm: 0.01, m: 1, km: 1e3, in: 0.0254, ft: 0.3048, yd: 0.9144, mi: 1609.344 };\n'
        'var MASS = { mg: 1e-6, g: 0.001, kg: 1, t: 1000, oz: 0.028349523125, lb: 0.45359237 };\n'
        '\n'
        'var SYMBOLS = {\n'
        '  copyright: "\\251 2019",\n'
        "  degree: '\\u00B0',\n"
        '  micro: "\\xB5",\n'
        "  ohm: '\\u{2126}',\n"
        "  rocket: '\\u{1F680}',\n"
        "  half: '\\uD83D',\n"
        '  pair: "\\uD83D\\uDE80",\n'
        "  tab: 'a\\tb',\n"
        "  nul: '\\0',\n"
        "  quote: 'it\\'s',\n"
        "  continued: 'line one \\\n"
        "line two',\n"
        "  vertical: '\\v\\f\\b'\n"
        '};\n'
        '\n'
        'function convert(value, from, to, table) {\n'
        '  if (!(from in table) || !(to in table)) {\n'
        "    throw new RangeError('unknown unit: ' + (from in table ? to : from));\n"
        '  }\n'
        '  return value * table[from] / table[to];\n'
        '}\n'
        '\n'
        'function celsius(f) { return (f - 32) * 5 / 9; }\n'
        'var fahrenheit = function (c) { return c * 9 / 5 + 32; };\n'
        '\n'
        "var π = Math.PI, café = 'open', 数量 = 42, ℮ = 2;\n"
        'var $dollar = 1, _under = 2, \\u0061bc = 3;\n'
        '\n'
        '<!-- an HTML-style comment, which scripts allow\n'
        "var shown = convert(3, 'ft', 'm', LENGTH) + MODE_DEFAULT - MODE_EXEC + (MASK & 0x1F);\n"
        '--> and the closing form, at the start of a line\n',
    'snip/arrow_strict_directive.js':
        "f = (a = 1) => { 'use strict'; };\n",
    'snip/arrows.js':
        'f = () => {}; g = x => x * 2; h = (a, b = 1, ...rest) => ({a, b, rest});\n',
    'snip/asi.js':
        'a = b\n'
        '(c)\n'
        'd = e\n'
        '++f\n'
        'g\n'
        'if (h) i(); else j()\n',
    'snip/assign.js':
        'answer = 6 * 7;\n',
    'snip/assign_patterns.js':
        '[a, b] = [b, a]; ({x: obj.x, y = 5} = point);\n',
    'snip/async_arrows.js':
        'p = async () => await q; r = async x => x; s = async (y) => { await y; }; t = async(1, 2);\n',
    'snip/async_newline.js':
        'async\n'
        'function f() {}\n',
    'snip/await_module.js':
        'var await = 1;\n',
    'snip/await_script.js':
        'var await = 1; await(2);\n',
    'snip/chain.js':
        'a.b[c](d).e`t${f}`;\n',
    'snip/class_async_gen.js':
        'class A { async *w() {} }\n',
    'snip/class_expr.js':
        'const C = class Named {}; const D = class extends (mixin(A, B)) {};\n',
    'snip/class_full.js':
        "class A extends B { constructor() { super(); } static create() { return new A(); } get x() { return 1; } set x(v) {} *gen() {} async run() {} ['computed' + 1]() {} 'quoted'() {} 42() {} static get y() {} static async z() {} }\n",
    'snip/class_props.js':
        'class A { x; y = 1; static z = 2; m() {} static n; }\n',
    'snip/class_props_computed.js':
        'class A { [k] = 4; }\n',
    'snip/class_props_quoted.js':
        "class A { 'q' = 3; }\n",
    'snip/comment_crash.js':
        'if (a) { /* c */ } // d\n'
        '{ }\n',
    'snip/comment_only.js':
        '// only a comment\n',
    'snip/comments_attach.js':
        '/* lead */ function f(/* p */ a) { // body\n'
        '  /* inner */\n'
        '} // trail\n'
        'var x = 1; /* after x */\n',
    'snip/comments_both.js':
        "import x from 'x'; // why x\n"
        '// leading for f\n'
        'export function f() {\n'
        '  return x; // trailing for return\n'
        '}\n'
        '/* dangling */\n',
    'snip/comments_collect.js':
        '// first\n'
        'a = 1; /* second */ b = 2;\n'
        '/** third\n'
        ' * spans */\n',
    'snip/conditional.js':
        'ok = a ? b : c ? d : e;\n',
    'snip/crlf.js':
        'a = 1;\r\n'
        'b = 2;\r\n'
        '\rc = 3;\n',
    'snip/destructure.js':
        'const {a, b: {c = 1}, ...d} = obj; let [x, , y = 2, ...z] = arr;\n',
    'snip/directive_empty.js':
        "''; 'x'\n",
    'snip/directives.js':
        '\'use strict\'; "another"; \'use strict\'.length; function f() { "use strict"; return this; }\n',
    'snip/dup_constructor.js':
        'class A { constructor() {} constructor() {} }\n',
    'snip/dup_proto.js':
        "o = ({__proto__: 1, __proto__: 2, ['__proto__']: 3});\n",
    'snip/err_arrow_dupe.js':
        'f = (a, a) => 1;\n',
    'snip/err_arrow_eval.js':
        "'use strict'; f = (eval) => 1;\n",
    'snip/err_arrow_rest.js':
        'f = (...a, b) => 1;\n',
    'snip/err_binary_digit.js':
        'x = 0b12;\n',
    'snip/err_break.js':
        'break;\n',
    'snip/err_class_no_name.js':
        'class { }\n',
    'snip/err_close_paren.js':
        ')\n',
    'snip/err_code_point.js':
        "s = '\\u{110000}';\n",
    'snip/err_const_init.js':
        'const a;\n',
    'snip/err_exponent.js':
        'x = 1e;\n',
    'snip/err_export_default_ref.js':
        'export {default};\n',
    'snip/err_hex_empty.js':
        'x = 0x;\n',
    'snip/err_hex_escape.js':
        "s = '\\x4';\n",
    'snip/err_ident_after_number.js':
        'x = 3in y;\n',
    'snip/err_ident_escape.js':
        'var \\u0030abc;\n',
    'snip/err_import_no_from.js':
        'import {a};\n',
    'snip/err_label_redecl.js':
        'foo: foo: ;\n',
    'snip/err_let_bracket.js':
        'let[0] = 2;\n',
    'snip/err_let_let.js':
        'let let = 1;\n',
    'snip/err_missing_expr.js':
        'a = ;\n',
    'snip/err_new_target.js':
        'x = new.target;\n',
    'snip/err_number_ident.js':
        'var 1x;\n',
    'snip/err_open_brace.js':
        '{\n',
    'snip/err_paren.js':
        'if (a { }\n',
    'snip/err_template_octal.js':
        't = `\\01`;\n',
    'snip/err_throw_newline.js':
        'throw\n'
        'new Error();\n',
    'snip/err_try_alone.js':
        'try {}\n',
    'snip/err_two_defaults.js':
        'switch (x) { default: default: }\n',
    'snip/err_unicode_escape.js':
        "s = '\\u12';\n",
    'snip/err_unknown_label.js':
        'continue foo;\n',
    'snip/err_unterminated_comment.js':
        '/* abc\n',
    'snip/err_unterminated_regex.js':
        'x = /abc\n',
    'snip/err_unterminated_string.js':
        "'abc\n",
    'snip/err_unterminated_template.js':
        '`abc\n',
    'snip/err_yield_var.js':
        'function* g() { var yield; }\n',
    'snip/escaped_keyword.js':
        'v\\u0061r x = 1; var a\\u0024 = 2;\n',
    'snip/export_default_class.js':
        'export default class {}\n',
    'snip/export_default_expr.js':
        'export default (a, b);\n',
    'snip/export_defaults.js':
        'export default async function () {}\n',
    'snip/exports.js':
        "export var v = 1; export let l = 2; export const c = 3; export function f() {} export class K {} export {v as w, l}; export * from 'all'; export {default, x as y} from 'mod'; export async function af() {}\n",
    'snip/for_in_init.js':
        'for (var [a, b] = [1, 2] in c);\n',
    'snip/for_in_seq.js':
        'for (a in b, c) ;\n',
    'snip/for_let_in.js':
        'for (let in obj) {}\n',
    'snip/for_loops.js':
        'for (var i = 0, n = a.length; i < n; i++) {} for (const k in o) {} for (let v of list) {} for (x of y); for (;;) break;\n',
    'snip/getter_arity.js':
        'o = ({ get a(x) {}, set b() {}, set c(...d) {} });\n',
    'snip/getter_constructor.js':
        'class A { get constructor() {} }\n',
    'snip/html_comment_module.js':
        'a <!-- b;\n',
    'snip/illegal_return.js':
        'return 1;\n',
    'snip/import_call.js':
        "import('./lazy.js').then(m => m.default);\n",
    'snip/import_in_script.js':
        "import x from 'y'; export default 1;\n",
    'snip/label_function.js':
        'foo: function f() {}\n',
    'snip/label_generator.js':
        'foo: function* g() {}\n',
    'snip/labels.js':
        'outer: while (true) { inner: do { continue outer; } while (false); break outer; }\n',
    'snip/let_forms.js':
        'let = 1; let.x = 2; var let;\n',
    'snip/modules.js':
        "import a from 'a'; import * as b from 'b'; import {c, d as e, default as f} from 'c'; import g, {h} from 'g'; import i, * as j from 'i'; import 'side-effect';\n",
    'snip/new.js':
        'new Date; new Foo.Bar(1)(2); new new X()();\n',
    'snip/new_target.js':
        'function F() { return new.target; }\n',
    'snip/numbers_all.js':
        'n = [0xFFFFFFFFFFFFFFFFFFFF, 1e21, 1e400, 5e-324, 0.1, 017, 0o17, 0b11, .5e1, 2e-7, 1.7976931348623157e308, 123456789012345678901234567890, 0.30000000000000004];\n',
    'snip/numbers_odd.js':
        'a = 08.5; b = 09; c = 1..toString(); d = 0.0; e = 00; f = 0O17;\n',
    'snip/object_full.js':
        "o = {a, b: 1, 'c': 2, 3: 4, [d]: 5, e() {}, get f() { return 1; }, set f(v) {}, *g() {}, async h() {}, async: 1, get: 2, set: 3, ...rest};\n",
    'snip/octal_escapes.js':
        "s = ['\\0', '\\08', '\\12', '\\377', '\\400', '\\a'];\n",
    'snip/octal_escapes_tolerant.js':
        "s = ['\\8', '\\9'];\n",
    'snip/operators.js':
        'x = a || b && c | d ^ e & f == g != h === i !== j < k > l <= m >= n instanceof o in p << q >> r >>> s;\n',
    'snip/precedence.js':
        'r = a + b * c - d / e % f ** g ** h;\n',
    'snip/regex_astral.js':
        'e = /\\u{1F600}+/u; f = /\\uD83D\\uDE00|x/; g = /[\\u0041-\\u005A]/i;\n',
    'snip/regex_basic.js':
        'r = /ab+c/gi; s = /[/]/; t = /\\d{3}-\\d{4}/m; u = /a/y; w = /^\\s*$/;\n',
    'snip/regex_flag_escape.js':
        'r = /a/\\u0067;\n',
    'snip/regex_named_group.js':
        'm = /(?<year>\\d{4})-(?<month>\\d{2})/u.exec(s);\n',
    'snip/regex_named_group_tolerant.js':
        'm = /(?<year>\\d{4})/u; n = /[^]/; o = /\\cJ/; ok = /(?:a|b)+/;\n',
    'snip/source_option.js':
        'export const pi = 3.14159;\n',
    'snip/static_prototype.js':
        'class A { static prototype() {} }\n',
    'snip/strict_delete.js':
        "'use strict'; delete x;\n",
    'snip/strict_dupe_params.js':
        "'use strict'; function f(a, a) {}\n",
    'snip/strict_eval.js':
        "'use strict'; eval = 1;\n",
    'snip/strict_octal.js':
        "'use strict'; var x = 017;\n",
    'snip/strict_octal_escape.js':
        "'\\12'; 'use strict'; t = '\\7';\n",
    'snip/strict_tolerant.js':
        'with (x) {} delete y; eval = 1; var z = 017; function g(a, a) {} arguments++;\n',
    'snip/strict_with.js':
        "'use strict'; with (a) {}\n",
    'snip/switch_try.js':
        'switch (x) { case 1: case 2: y(); break; default: z(); } try { a(); } catch (e) { b(e); } finally { c(); }\n',
    'snip/tagged_raw.js':
        's = String.raw`C:\\temp\\${x}\\u`;\n',
    'snip/template_cooked.js':
        't = `\\u{1F600}${a}\\0`; u = `\\uzz`;\n',
    'snip/templates.js':
        't = `a${b}c${`nested ${d}`}e`; u = `\\n\\x41\\u{42}\\u0043`; v = `line\n'
        'two`;\n',
    'snip/tok_block_regex.js':
        '{} /x/; a = {} /x/',
    'snip/tok_comments.js':
        '/* a */ x // b\n'
        '<!-- c\n'
        '--> d\n'
        'y',
    'snip/tok_crash_curly.js':
        'a b } /x/',
    'snip/tok_crash_paren.js':
        ') /x/',
    'snip/tok_division.js':
        'this / 2 / 3; [] / 2; x = a / b / c',
    'snip/tok_function_regex.js':
        'function(){} /42/i',
    'snip/tok_keywords.js':
        'let yield await async of get set static',
    'snip/tok_named_function_div.js':
        'x = function f(){} /1/ g',
    'snip/tok_paren_regex.js':
        'a b ) /x/',
    'snip/tok_regex_after_if.js':
        'if (a) /b/.test(c)',
    'snip/tok_regex_fallback.js':
        'x = 1 /(/ 2',
    'snip/tok_regex_invalid_python.js':
        'x = /(?<n>a)/; y = /[^]/',
    'snip/tok_template.js':
        '`a${b}c${d}e` + `plain`',
    'snip/tok_unterminated.js':
        "'abc",
    'snip/tok_unterminated_tolerant.js':
        "x = 'abc",
    'snip/tokens_loc.js':
        'let a = `x${b}y`; // done\n',
    'snip/tokens_option.js':
        'if (x) y = /re/g.test(z) / 2;\n',
    'snip/tolerant_many.js':
        'var a = 1 +; if (b c; while (d { } x = 5\n',
    'snip/trailing_commas.js':
        'x = {a: 1,}; f(a, b,); y = [1, 2, , ];\n',
    'snip/unary.js':
        '!a; -b; +c; ~d; typeof e; void f; delete g.h; ++i; j--; - -k;\n',
    'snip/unicode_strings.js':
        "s = ['caf\\u00e9', '\\u{1F680}', '\\uD83D', 'тест', '数量', '\\\\'];\n",
    'snip/whitespace.js':
        ' \xa0 \ufeff var x\u2028= 1;\u2029y = 2\n',
    'snip/with_debugger.js':
        'with (obj) { debugger; }\n',
    'snip/yield_forms.js':
        'function* g() { yield; yield a; yield* b; x = yield; }\n'
        'var yield = 1;\n',
    'tools/report.js':
        "'use strict';\n"
        '// node tools/report.js <log> [--top N] [--since YYYY-MM-DD]\n'
        "const fs = require('fs');\n"
        "const path = require('path');\n"
        "const { promisify } = require('util');\n"
        '\n'
        'const readFile = promisify(fs.readFile);\n'
        'const LINE = /^(\\S+) \\S+ \\S+ \\[([^\\]]+)\\] "(\\w+) ([^"]*?) HTTP\\/[\\d.]+" (\\d{3}) (\\d+|-)/;\n'
        '\n'
        'function parseArgs(argv) {\n'
        '  const opts = { top: 10, since: null, files: [] };\n'
        '  for (let i = 0; i < argv.length; i++) {\n'
        '    const arg = argv[i];\n'
        '    switch (arg) {\n'
        "      case '--top':\n"
        '        opts.top = parseInt(argv[++i], 10);\n'
        '        break;\n'
        "      case '--since':\n"
        '        opts.since = new Date(argv[++i]);\n'
        '        break;\n'
        '      default:\n'
        "        if (arg.startsWith('--')) {\n"
        "          throw new Error('unknown option ' + arg);\n"
        '        }\n'
        '        opts.files.push(path.resolve(arg));\n'
        '    }\n'
        '  }\n'
        '  return opts;\n'
        '}\n'
        '\n'
        'function tally(lines, since) {\n'
        '  const byPath = Object.create(null);\n'
        '  let bytes = 0, errors = 0, skipped = 0;\n'
        '  outer: for (const line of lines) {\n'
        '    const m = LINE.exec(line);\n'
        '    if (!m) {\n'
        '      skipped++;\n'
        '      continue;\n'
        '    }\n'
        '    const [, ip, when, method, url, status, size] = m;\n'
        "    if (since && new Date(when.replace(':', ' ')) < since) continue outer;\n"
        "    const key = method + ' ' + url.split('?')[0];\n"
        '    const entry = byPath[key] || (byPath[key] = { hits: 0, bytes: 0, ips: new Set() });\n'
        '    entry.hits += 1;\n'
        '    entry.ips.add(ip);\n'
        "    if (size !== '-') {\n"
        '      entry.bytes += +size;\n'
        '      bytes += +size;\n'
        '    }\n'
        "    if (status[0] === '5') errors++;\n"
        '  }\n'
        '  return { byPath, bytes, errors, skipped };\n'
        '}\n'
        '\n'
        'async function main() {\n'
        '  const opts = parseArgs(process.argv.slice(2));\n'
        "  const texts = await Promise.all(opts.files.map((f) => readFile(f, 'utf8')));\n"
        '  const lines = [].concat(...texts.map((t) => t.split(/\\r?\\n/)));\n'
        '  const { byPath, bytes, errors, skipped } = tally(lines, opts.since);\n'
        '  const rows = Object.keys(byPath)\n'
        '    .map((k) => [k, byPath[k]])\n'
        '    .sort((a, b) => b[1].hits - a[1].hits || (a[0] < b[0] ? -1 : 1))\n'
        '    .slice(0, opts.top);\n'
        '  for (const [key, { hits, bytes: b, ips }] of rows) {\n'
        '    console.log(`${String(hits).padStart(7)}  ${String(ips.size).padStart(5)}  ${(b / 1024).toFixed(1).padStart(9)}K  ${key}`);\n'
        '  }\n'
        '  console.log(`${lines.length} lines, ${skipped} skipped, ${errors} 5xx, ${bytes} bytes`);\n'
        '}\n'
        '\n'
        'if (require.main === module) {\n'
        '  main().catch((err) => {\n'
        '    console.error(err.stack || String(err));\n'
        '    process.exitCode = 1;\n'
        '  });\n'
        '}\n'
        '\n'
        'module.exports = { parseArgs, tally };\n',
}

JOBS = [
    ('tree', 'snip/assign.js', 'script', ''),
    ('tree', 'snip/precedence.js', 'script', ''),
    ('tree', 'snip/operators.js', 'script', ''),
    ('tree', 'snip/conditional.js', 'script', 'range'),
    ('tree', 'snip/unary.js', 'script', ''),
    ('tree', 'snip/new.js', 'script', ''),
    ('tree', 'snip/chain.js', 'script', ''),
    ('tree', 'snip/arrows.js', 'script', ''),
    ('tree', 'snip/async_arrows.js', 'script', ''),
    ('tree', 'snip/destructure.js', 'script', ''),
    ('tree', 'snip/assign_patterns.js', 'script', ''),
    ('tree', 'snip/for_loops.js', 'script', ''),
    ('tree', 'snip/for_let_in.js', 'script', ''),
    ('tree', 'snip/class_full.js', 'script', ''),
    ('tree', 'snip/class_expr.js', 'script', ''),
    ('tree', 'snip/object_full.js', 'script', ''),
    ('tree', 'snip/templates.js', 'script', 'range'),
    ('tree', 'snip/tagged_raw.js', 'script', ''),
    ('tree', 'snip/regex_basic.js', 'script', ''),
    ('tree', 'snip/regex_named_group.js', 'script', ''),
    ('tree', 'snip/regex_named_group_tolerant.js', 'script', 'tolerant'),
    ('tree', 'snip/regex_astral.js', 'script', ''),
    ('tree', 'snip/regex_flag_escape.js', 'script', 'tolerant'),
    ('tree', 'snip/switch_try.js', 'script', ''),
    ('tree', 'snip/labels.js', 'script', ''),
    ('tree', 'snip/with_debugger.js', 'script', ''),
    ('tree', 'snip/asi.js', 'script', 'loc'),
    ('tree', 'snip/directives.js', 'script', ''),
    ('tree', 'snip/directive_empty.js', 'script', ''),
    ('tree', 'snip/strict_with.js', 'script', ''),
    ('tree', 'snip/strict_octal.js', 'script', ''),
    ('tree', 'snip/strict_delete.js', 'script', ''),
    ('tree', 'snip/strict_eval.js', 'script', ''),
    ('tree', 'snip/strict_dupe_params.js', 'script', ''),
    ('tree', 'snip/strict_tolerant.js', 'module', 'tolerant'),
    ('tree', 'snip/illegal_return.js', 'script', 'tolerant'),
    ('tree', 'snip/err_number_ident.js', 'script', ''),
    ('tree', 'snip/err_paren.js', 'script', ''),
    ('tree', 'snip/err_missing_expr.js', 'script', ''),
    ('tree', 'snip/err_open_brace.js', 'script', ''),
    ('tree', 'snip/err_close_paren.js', 'script', ''),
    ('tree', 'snip/err_class_no_name.js', 'script', ''),
    ('tree', 'snip/err_let_let.js', 'script', ''),
    ('tree', 'snip/err_const_init.js', 'script', ''),
    ('tree', 'snip/err_break.js', 'script', ''),
    ('tree', 'snip/err_unknown_label.js', 'script', ''),
    ('tree', 'snip/err_label_redecl.js', 'script', ''),
    ('tree', 'snip/err_two_defaults.js', 'script', ''),
    ('tree', 'snip/err_try_alone.js', 'script', ''),
    ('tree', 'snip/err_throw_newline.js', 'script', ''),
    ('tree', 'snip/err_new_target.js', 'script', ''),
    ('tree', 'snip/import_in_script.js', 'script', 'tolerant'),
    ('tree', 'snip/err_unterminated_string.js', 'script', ''),
    ('tree', 'snip/err_unterminated_template.js', 'script', ''),
    ('tree', 'snip/err_unterminated_comment.js', 'script', ''),
    ('tree', 'snip/err_unterminated_regex.js', 'script', ''),
    ('tree', 'snip/err_hex_escape.js', 'script', ''),
    ('tree', 'snip/err_unicode_escape.js', 'script', ''),
    ('tree', 'snip/err_code_point.js', 'script', ''),
    ('tree', 'snip/err_ident_escape.js', 'script', ''),
    ('tree', 'snip/escaped_keyword.js', 'script', 'tolerant'),
    ('tree', 'snip/err_hex_empty.js', 'script', ''),
    ('tree', 'snip/err_binary_digit.js', 'script', ''),
    ('tree', 'snip/numbers_odd.js', 'script', ''),
    ('tree', 'snip/err_exponent.js', 'script', ''),
    ('tree', 'snip/err_ident_after_number.js', 'script', ''),
    ('tree', 'snip/numbers_all.js', 'script', ''),
    ('tree', 'snip/modules.js', 'module', ''),
    ('tree', 'snip/exports.js', 'module', ''),
    ('tree', 'snip/export_defaults.js', 'module', ''),
    ('tree', 'snip/export_default_class.js', 'module', ''),
    ('tree', 'snip/export_default_expr.js', 'module', ''),
    ('tree', 'snip/err_export_default_ref.js', 'module', ''),
    ('tree', 'snip/err_import_no_from.js', 'module', ''),
    ('tree', 'snip/import_call.js', 'script', ''),
    ('tree', 'snip/comments_attach.js', 'script', 'attach'),
    ('tree', 'snip/comments_collect.js', 'script', 'comment,range,loc'),
    ('tree', 'snip/comment_only.js', 'script', 'attach,comment'),
    ('tree', 'snip/comments_both.js', 'module', 'attach,comment,range'),
    ('tree', 'snip/html_comment_module.js', 'module', ''),
    ('tree', 'snip/getter_arity.js', 'script', 'tolerant'),
    ('tree', 'snip/dup_constructor.js', 'script', ''),
    ('tree', 'snip/static_prototype.js', 'script', ''),
    ('tree', 'snip/getter_constructor.js', 'script', ''),
    ('tree', 'snip/dup_proto.js', 'script', 'tolerant'),
    ('tree', 'snip/yield_forms.js', 'script', ''),
    ('tree', 'snip/err_yield_var.js', 'script', ''),
    ('tree', 'snip/await_script.js', 'script', ''),
    ('tree', 'snip/await_module.js', 'module', 'tolerant'),
    ('tree', 'snip/async_newline.js', 'script', ''),
    ('tree', 'snip/arrow_strict_directive.js', 'script', 'tolerant'),
    ('tree', 'snip/err_arrow_rest.js', 'script', ''),
    ('tree', 'snip/err_arrow_dupe.js', 'script', ''),
    ('tree', 'snip/err_arrow_eval.js', 'script', ''),
    ('tree', 'snip/trailing_commas.js', 'script', ''),
    ('tree', 'snip/for_in_seq.js', 'script', ''),
    ('tree', 'snip/for_in_init.js', 'script', 'tolerant'),
    ('tree', 'snip/whitespace.js', 'script', 'loc'),
    ('tree', 'snip/crlf.js', 'script', 'loc,range'),
    ('tree', 'snip/class_props.js', 'script', 'classProps'),
    ('tree', 'snip/class_props_computed.js', 'script', 'classProps'),
    ('tree', 'snip/class_props_quoted.js', 'script', 'classProps'),
    ('tree', 'snip/class_async_gen.js', 'script', ''),
    ('tree', 'snip/source_option.js', 'module', 'loc,source'),
    ('tree', 'snip/new_target.js', 'script', ''),
    ('tree', 'snip/label_function.js', 'script', ''),
    ('tree', 'snip/label_generator.js', 'script', 'tolerant'),
    ('tree', 'snip/let_forms.js', 'script', ''),
    ('tree', 'snip/err_let_bracket.js', 'script', ''),
    ('tree', 'snip/octal_escapes.js', 'script', ''),
    ('tree', 'snip/octal_escapes_tolerant.js', 'script', 'tolerant'),
    ('tree', 'snip/strict_octal_escape.js', 'script', 'tolerant'),
    ('tree', 'snip/template_cooked.js', 'script', ''),
    ('tree', 'snip/err_template_octal.js', 'script', ''),
    ('tree', 'snip/unicode_strings.js', 'script', ''),
    ('tree', 'snip/tokens_option.js', 'script', 'tokens,range'),
    ('tree', 'snip/tokens_loc.js', 'module', 'tokens,loc,comment'),
    ('tree', 'snip/comment_crash.js', 'script', 'attach'),
    ('tree', 'snip/tolerant_many.js', 'script', 'tolerant'),
    ('tokens', 'snip/tok_regex_after_if.js', 'script', ''),
    ('tokens', 'snip/tok_division.js', 'script', 'range'),
    ('tokens', 'snip/tok_function_regex.js', 'script', ''),
    ('tokens', 'snip/tok_named_function_div.js', 'script', ''),
    ('tokens', 'snip/tok_block_regex.js', 'script', ''),
    ('tokens', 'snip/tok_paren_regex.js', 'script', ''),
    ('tokens', 'snip/tok_crash_curly.js', 'script', ''),
    ('tokens', 'snip/tok_crash_paren.js', 'script', 'tolerant'),
    ('tokens', 'snip/tok_unterminated.js', 'script', ''),
    ('tokens', 'snip/tok_unterminated_tolerant.js', 'script', 'tolerant'),
    ('tokens', 'snip/tok_comments.js', 'script', 'comment,range,loc'),
    ('tokens', 'snip/tok_template.js', 'script', 'range'),
    ('tokens', 'snip/tok_regex_invalid_python.js', 'script', 'tolerant'),
    ('tokens', 'snip/tok_regex_fallback.js', 'script', ''),
    ('tokens', 'snip/tok_keywords.js', 'script', ''),
    ('digest', 'app/server.js', 'module', ''),
    ('digest', 'app/router.js', 'module', ''),
    ('digest', 'app/db.js', 'module', ''),
    ('digest', 'app/util.js', 'module', ''),
    ('digest', 'app/config.js', 'module', ''),
    ('digest', 'legacy/tabs.js', 'script', ''),
    ('digest', 'legacy/polyfill.js', 'script', ''),
    ('digest', 'tools/report.js', 'script', ''),
    ('digest', 'lib/csv.js', 'script', ''),
    ('digest', 'lib/events.js', 'module', ''),
    ('digest', 'lib/queue.js', 'module', 'classProps'),
    ('digest', 'lib/units.js', 'script', ''),
    ('digest', 'lib/iter.js', 'script', ''),
    ('digest', 'lib/queue.js', 'module', ''),
    ('digest', 'app/server.js', 'module', 'range,loc,tokens,comment'),
    ('digest', 'legacy/tabs.js', 'script', 'attach,comment,range'),
    ('digest', 'lib/csv.js', 'script', 'attach,loc'),
    ('digest', 'lib/units.js', 'script', 'tolerant,loc,source'),
    ('digest', 'lib/units.js', 'module', 'tolerant'),
    ('digest', 'app/router.js', 'script', 'tolerant'),
    ('tree', 'app/config.js', 'module', ''),
    ('tree', 'lib/events.js', 'module', 'attach'),
    ('tokens-digest', 'app/util.js', 'module', ''),
    ('tokens-digest', 'legacy/polyfill.js', 'script', 'comment,range,loc'),
    ('tokens-digest', 'lib/units.js', 'script', 'comment,loc'),
    ('tokens-digest', 'tools/report.js', 'script', 'range'),
    ('outline', 'app/server.js', 'module', ''),
    ('outline', 'app/router.js', 'module', ''),
    ('outline', 'app/db.js', 'module', ''),
    ('outline', 'app/util.js', 'module', ''),
    ('outline', 'app/config.js', 'module', ''),
    ('outline', 'legacy/tabs.js', 'script', ''),
    ('outline', 'legacy/polyfill.js', 'script', ''),
    ('outline', 'tools/report.js', 'script', ''),
    ('outline', 'lib/csv.js', 'script', ''),
    ('outline', 'lib/events.js', 'module', ''),
    ('outline', 'lib/queue.js', 'module', ''),
    ('outline', 'lib/units.js', 'script', ''),
    ('outline', 'lib/iter.js', 'script', ''),
    ('stats', 'app/server.js', 'module', ''),
    ('stats', 'app/router.js', 'module', ''),
    ('stats', 'app/db.js', 'module', ''),
    ('stats', 'app/util.js', 'module', ''),
    ('stats', 'app/config.js', 'module', ''),
    ('stats', 'legacy/tabs.js', 'script', ''),
    ('stats', 'legacy/polyfill.js', 'script', ''),
    ('stats', 'tools/report.js', 'script', ''),
    ('stats', 'lib/csv.js', 'script', ''),
    ('stats', 'lib/events.js', 'module', ''),
    ('stats', 'lib/queue.js', 'module', ''),
    ('stats', 'lib/units.js', 'script', ''),
    ('stats', 'lib/iter.js', 'script', ''),
    ('graph', 'app/server.js+app/router.js+app/db.js+app/util.js+app/config.js', 'module', ''),
    ('graph', 'lib/queue.js+lib/events.js', 'module', ''),
    ('graph', 'app/server.js+app/router.js+lib/queue.js', 'module', ''),
]


def main():
    for path, text in SOURCES.items():
        full = os.path.join("data", "src", path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    with open(os.path.join("data", "jobs.tsv"), "w", encoding="utf-8") as f:
        for i, (op, path, mode, opts) in enumerate(JOBS, 1):
            f.write("%d\t%s\t%s\t%s\t%s\n" % (i, op, path, mode, opts))


main()
