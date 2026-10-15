// Runs data/jobs.txt with the real semver 7.7.2: `semver` jobs run its
// command-line tool, `lib` jobs call the library, and `outdated` builds a
// dependency report from a package.json, its lock file and a registry
// index. Run with node from the app's directory.
'use strict'
const fs = require('fs')
const path = require('path')
const { spawnSync } = require('child_process')
const MOD = path.join(__dirname, 'realnode/node_modules/semver')
const semver = require(MOD)
const DATA = process.argv[2] || 'data'

// A job's words: split on spaces, with "..." for a word holding spaces.
const words = (line) => {
  const out = []
  let i = 0
  while (i < line.length) {
    if (line[i] === ' ') { i++; continue }
    if (line[i] === '"') {
      const j = line.indexOf('"', i + 1)
      out.push(line.slice(i + 1, j))
      i = j + 1
    } else {
      let j = i
      while (j < line.length && line[j] !== ' ') j++
      out.push(line.slice(i, j))
      i = j
    }
  }
  return out
}

const show = (v) => v === null ? 'null' : String(v)

const opts = (args) => {
  const o = {}
  const rest = []
  for (const a of args) {
    if (a === '--loose') o.loose = true
    else if (a === '-p') o.includePrerelease = true
    else if (a === '--rtl') o.rtl = true
    else rest.push(a)
  }
  return [o, rest]
}

const lib = (fn, args) => {
  const [o, a] = opts(args)
  try {
    switch (fn) {
      case 'parse': {
        const v = semver.parse(a[0], o)
        if (!v) return 'null'
        return `${v.major} ${v.minor} ${v.patch} pre=${JSON.stringify(v.prerelease)} build=${JSON.stringify(v.build)}`
      }
      case 'validRange': return show(semver.validRange(a[0], o))
      case 'minVersion': { const v = semver.minVersion(a[0], o); return v ? v.version : 'null' }
      case 'maxSatisfying': return show(semver.maxSatisfying(a.slice(1), a[0], o))
      case 'minSatisfying': return show(semver.minSatisfying(a.slice(1), a[0], o))
      case 'intersects': return show(semver.intersects(a[0], a[1], o))
      case 'diff': return show(semver.diff(a[0], a[1]))
      case 'compareBuild': return show(semver.compareBuild(a[0], a[1], o))
      case 'simplify': return show(semver.simplifyRange(a.slice(1), a[0], o))
      case 'coerce': { const v = semver.coerce(a[0], o); return v ? v.version : 'null' }
      case 'inc': return show(semver.inc(a[0], a[1], o, a[2], a[3] === 'false' ? false : a[3]))
    }
  } catch (e) {
    return `error: ${e.message}`
  }
  return `unknown function ${fn}`
}

// --- outdated

const pick = (pk, spec) => {
  const tags = pk['dist-tags'] || {}
  if (semver.validRange(spec) === null) {
    if (Object.prototype.hasOwnProperty.call(tags, spec)) return tags[spec]
    return 'INVALID'
  }
  if (tags.latest && semver.satisfies(tags.latest, spec)) return tags.latest
  const dep = pk.deprecated || {}
  const live = pk.versions.filter(v => !Object.prototype.hasOwnProperty.call(dep, v))
  return semver.maxSatisfying(live, spec) || semver.maxSatisfying(pk.versions, spec) || 'NONE'
}

const table = (rows) => {
  const w = rows[0].map((_, i) => Math.max(...rows.map(r => r[i].length)))
  return rows.map(r => r.map((c, i) => c.padEnd(w[i])).join('  ').trimEnd()).join('\n') + '\n'
}

const outdated = (dir) => {
  const pj = JSON.parse(fs.readFileSync(path.join(DATA, dir, 'package.json'), 'utf8'))
  const lock = JSON.parse(fs.readFileSync(path.join(DATA, dir, 'package-lock.json'), 'utf8'))
  const reg = JSON.parse(fs.readFileSync(path.join(DATA, 'registry.json'), 'utf8'))
  const deps = []
  for (const kind of ['dependencies', 'devDependencies', 'optionalDependencies']) {
    for (const [name, spec] of Object.entries(pj[kind] || {})) deps.push([name, spec, kind])
  }
  deps.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)
  const rows = [['Package', 'Current', 'Wanted', 'Latest', 'Type']]
  const notes = []
  for (const [name, spec, kind] of deps) {
    const pk = reg[name]
    const entry = (lock.packages || {})['node_modules/' + name]
    const current = entry ? entry.version : 'MISSING'
    if (!pk) { notes.push(`${name}: not in the registry`); continue }
    const wanted = pick(pk, spec)
    const latest = (pk['dist-tags'] || {}).latest || 'NONE'
    if (current === wanted && current === latest) continue
    rows.push([name, current, wanted, latest, kind])
    if (wanted === 'INVALID') { notes.push(`${name}: "${spec}" is not a range or a dist-tag`); continue }
    if (wanted === 'NONE') { notes.push(`${name}: nothing satisfies "${spec}"`); continue }
    if (current !== 'MISSING' && semver.valid(current)) {
      if (semver.lt(current, wanted)) notes.push(`${name}: ${current} -> ${wanted} (${semver.diff(current, wanted)})`)
      else if (semver.gt(current, wanted)) notes.push(`${name}: ${current} is newer than "${spec}" allows; wanted ${wanted}`)
      if (!semver.satisfies(current, spec) && semver.validRange(spec) !== null) notes.push(`${name}: installed ${current} does not satisfy "${spec}"`)
    } else if (current === 'MISSING') {
      notes.push(`${name}: not installed; would install ${wanted}`)
    }
    if (semver.valid(wanted) && semver.gt(latest, wanted)) notes.push(`${name}: ${latest} is out of range "${spec}" (${semver.diff(wanted, latest)})`)
    const dep = pk.deprecated || {}
    if (Object.prototype.hasOwnProperty.call(dep, current)) notes.push(`${name}: ${current} is deprecated: ${dep[current]}`)
  }
  let out = rows.length > 1 ? table(rows) : 'everything is up to date\n'
  for (const n of notes) out += n + '\n'
  return out
}

let out = ''
for (const line of fs.readFileSync(path.join(DATA, 'jobs.txt'), 'utf8').split('\n')) {
  if (line === '' || line.startsWith('#')) continue
  out += `$ ${line}\n`
  const w = words(line)
  if (w[0] === 'semver') {
    const r = spawnSync('node', [path.join(MOD, 'bin/semver.js'), ...w.slice(1)], { encoding: 'utf8' })
    out += r.stdout + r.stderr
    if (r.status !== 0) out += `[exit status ${r.status}]\n`
  } else if (w[0] === 'lib') {
    out += lib(w[1], w.slice(2)) + '\n'
  } else if (w[0] === 'outdated') {
    out += outdated(w[1])
  }
  out += '\n'
}
process.stdout.write(out)
