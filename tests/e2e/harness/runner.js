/**
 * Lightweight Deterministic Test Runner for Scoreboard App E2E Suite
 * Supports describe, it, test, hooks, async tests, timeouts, and detailed ANSI summaries.
 */

const ANSI = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
};

class TestRunner {
  constructor() {
    this.suites = [];
    this.currentSuite = null;
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      errors: [],
      startTime: 0,
      endTime: 0,
    };
  }

  describe(name, fn) {
    const suite = {
      name,
      tests: [],
      beforeAllHooks: [],
      beforeEachHooks: [],
      afterEachHooks: [],
      afterAllHooks: [],
      parent: this.currentSuite,
      children: [],
    };

    if (this.currentSuite) {
      this.currentSuite.children.push(suite);
    } else {
      this.suites.push(suite);
    }

    const prevSuite = this.currentSuite;
    this.currentSuite = suite;
    try {
      fn();
    } finally {
      this.currentSuite = prevSuite;
    }
  }

  it(name, fn) {
    if (!this.currentSuite) {
      this.describe('Default Suite', () => {
        this.it(name, fn);
      });
      return;
    }
    this.currentSuite.tests.push({
      name,
      fn,
      suite: this.currentSuite,
    });
  }

  test(name, fn) {
    this.it(name, fn);
  }

  beforeAll(fn) {
    if (this.currentSuite) this.currentSuite.beforeAllHooks.push(fn);
  }

  beforeEach(fn) {
    if (this.currentSuite) this.currentSuite.beforeEachHooks.push(fn);
  }

  afterEach(fn) {
    if (this.currentSuite) this.currentSuite.afterEachHooks.push(fn);
  }

  afterAll(fn) {
    if (this.currentSuite) this.currentSuite.afterAllHooks.push(fn);
  }

  _collectHooks(suite, type) {
    const hooks = [];
    let curr = suite;
    while (curr) {
      if (type === 'beforeEach') {
        hooks.unshift(...curr.beforeEachHooks);
      } else if (type === 'afterEach') {
        hooks.push(...curr.afterEachHooks);
      }
      curr = curr.parent;
    }
    return hooks;
  }

  async _runSuite(suite, depth = 0) {
    const indent = '  '.repeat(depth);
    console.log(`${indent}${ANSI.bold}${ANSI.cyan}● ${suite.name}${ANSI.reset}`);

    // Run beforeAll
    for (const hook of suite.beforeAllHooks) {
      await hook();
    }

    // Run tests
    for (const test of suite.tests) {
      this.results.total++;
      const testIndent = '  '.repeat(depth + 1);
      const start = performance.now();

      // Run beforeEach
      const beforeHooks = this._collectHooks(suite, 'beforeEach');
      for (const bh of beforeHooks) {
        await bh();
      }

      let error = null;
      try {
        await test.fn();
      } catch (err) {
        error = err;
      }

      // Run afterEach
      const afterHooks = this._collectHooks(suite, 'afterEach');
      for (const ah of afterHooks) {
        try {
          await ah();
        } catch (e) {
          if (!error) error = e;
        }
      }

      const duration = (performance.now() - start).toFixed(2);

      if (error) {
        this.results.failed++;
        console.log(`${testIndent}${ANSI.red}✖ ${test.name}${ANSI.dim} (${duration}ms)${ANSI.reset}`);
        console.log(`${testIndent}  ${ANSI.red}${error.message}${ANSI.reset}`);
        if (error.stack) {
          const filteredStack = error.stack.split('\n').slice(1, 4).map(l => `${testIndent}    ${ANSI.dim}${l.trim()}${ANSI.reset}`).join('\n');
          console.log(filteredStack);
        }
        this.results.errors.push({ suite: suite.name, test: test.name, error });
      } else {
        this.results.passed++;
        console.log(`${testIndent}${ANSI.green}✔ ${test.name}${ANSI.dim} (${duration}ms)${ANSI.reset}`);
      }
    }

    // Run child suites
    for (const child of suite.children) {
      await this._runSuite(child, depth + 1);
    }

    // Run afterAll
    for (const hook of suite.afterAllHooks) {
      await hook();
    }
  }

  async run() {
    this.results.startTime = performance.now();
    console.log(`\n${ANSI.bold}${ANSI.blue}======================================================${ANSI.reset}`);
    console.log(`${ANSI.bold} SCOREBOARD APP — E2E TEST RUNNER${ANSI.reset}`);
    console.log(`${ANSI.bold}${ANSI.blue}======================================================${ANSI.reset}\n`);

    for (const suite of this.suites) {
      await this._runSuite(suite, 0);
    }

    this.results.endTime = performance.now();
    const totalDuration = ((this.results.endTime - this.results.startTime) / 1000).toFixed(3);

    console.log(`\n${ANSI.bold}------------------------------------------------------${ANSI.reset}`);
    console.log(`${ANSI.bold} SUMMARY:${ANSI.reset}`);
    console.log(`  Suites:   ${this.suites.length}`);
    console.log(`  Total:    ${this.results.total}`);
    console.log(`  Passed:   ${ANSI.green}${this.results.passed}${ANSI.reset}`);
    console.log(`  Failed:   ${this.results.failed > 0 ? ANSI.red : ANSI.dim}${this.results.failed}${ANSI.reset}`);
    console.log(`  Duration: ${totalDuration}s`);
    console.log(`${ANSI.bold}------------------------------------------------------${ANSI.reset}\n`);

    return this.results;
  }

  reset() {
    this.suites = [];
    this.currentSuite = null;
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      errors: [],
      startTime: 0,
      endTime: 0,
    };
  }
}

export const runner = new TestRunner();
export const describe = (name, fn) => runner.describe(name, fn);
export const it = (name, fn) => runner.it(name, fn);
export const test = (name, fn) => runner.test(name, fn);
export const beforeAll = (fn) => runner.beforeAll(fn);
export const beforeEach = (fn) => runner.beforeEach(fn);
export const afterEach = (fn) => runner.afterEach(fn);
export const afterAll = (fn) => runner.afterAll(fn);
