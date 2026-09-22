/**
 * Comprehensive Assertion Library for Scoreboard App E2E Test Suite
 */

function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  if (typeof a !== typeof b) return false;
  if (a === null || b === null || typeof a !== 'object') return false;

  if (Array.isArray(a) !== Array.isArray(b)) return false;
  if (Array.isArray(a)) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      if (!deepEqual(a[i], b[i])) return false;
    }
    return true;
  }

  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;

  for (const key of keysA) {
    if (!Object.prototype.hasOwnProperty.call(b, key)) return false;
    if (!deepEqual(a[key], b[key])) return false;
  }
  return true;
}

export class AssertionError extends Error {
  constructor(message, actual, expected) {
    super(message);
    this.name = 'AssertionError';
    this.actual = actual;
    this.expected = expected;
  }
}

export function expect(actual) {
  const matchers = (isNot = false) => ({
    toBe(expected) {
      const pass = Object.is(actual, expected);
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${JSON.stringify(actual)} ${isNot ? 'NOT ' : ''}to be ${JSON.stringify(expected)}`,
          actual,
          expected
        );
      }
    },

    toEqual(expected) {
      const pass = deepEqual(actual, expected);
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${JSON.stringify(actual)} ${isNot ? 'NOT ' : ''}to deeply equal ${JSON.stringify(expected)}`,
          actual,
          expected
        );
      }
    },

    toBeCloseTo(expected, precision = 2) {
      const diff = Math.abs(Number(actual) - Number(expected));
      const tolerance = Math.pow(10, -precision) / 2;
      const pass = diff < tolerance;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be close to ${expected} (precision ${precision}, diff ${diff})`,
          actual,
          expected
        );
      }
    },

    toContain(expected) {
      let pass = false;
      if (typeof actual === 'string') {
        pass = actual.includes(String(expected));
      } else if (Array.isArray(actual)) {
        pass = actual.some(item => deepEqual(item, expected) || item === expected);
      } else if (actual && typeof actual === 'object') {
        pass = Object.prototype.hasOwnProperty.call(actual, expected);
      }
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${JSON.stringify(actual)} ${isNot ? 'NOT ' : ''}to contain ${JSON.stringify(expected)}`,
          actual,
          expected
        );
      }
    },

    toBeGreaterThan(expected) {
      const pass = actual > expected;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be greater than ${expected}`,
          actual,
          expected
        );
      }
    },

    toBeGreaterThanOrEqual(expected) {
      const pass = actual >= expected;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be greater than or equal to ${expected}`,
          actual,
          expected
        );
      }
    },

    toBeLessThan(expected) {
      const pass = actual < expected;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be less than ${expected}`,
          actual,
          expected
        );
      }
    },

    toBeLessThanOrEqual(expected) {
      const pass = actual <= expected;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be less than or equal to ${expected}`,
          actual,
          expected
        );
      }
    },

    toBeTruthy() {
      const pass = Boolean(actual);
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be truthy`,
          actual,
          true
        );
      }
    },

    toBeFalsy() {
      const pass = !actual;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be falsy`,
          actual,
          false
        );
      }
    },

    toBeNull() {
      const pass = actual === null;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be null`,
          actual,
          null
        );
      }
    },

    toBeUndefined() {
      const pass = actual === undefined;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected ${actual} ${isNot ? 'NOT ' : ''}to be undefined`,
          actual,
          undefined
        );
      }
    },

    toBeDefined() {
      const pass = actual !== undefined;
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected value ${isNot ? 'NOT ' : ''}to be defined`,
          actual,
          'defined'
        );
      }
    },

    toMatch(pattern) {
      const regex = typeof pattern === 'string' ? new RegExp(pattern) : pattern;
      const pass = regex.test(String(actual));
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected "${actual}" ${isNot ? 'NOT ' : ''}to match pattern ${pattern}`,
          actual,
          pattern
        );
      }
    },

    toThrow(expectedError) {
      if (typeof actual !== 'function') {
        throw new AssertionError('Expected a function to test toThrow', actual, 'function');
      }
      let threw = false;
      let error = null;
      try {
        actual();
      } catch (err) {
        threw = true;
        error = err;
      }
      if (isNot) {
        if (threw) {
          throw new AssertionError(`Expected function NOT to throw, but it threw: ${error.message}`, error, null);
        }
      } else {
        if (!threw) {
          throw new AssertionError('Expected function to throw an error, but it did not', null, expectedError);
        }
        if (expectedError) {
          if (typeof expectedError === 'string' && !error.message.includes(expectedError)) {
            throw new AssertionError(
              `Expected thrown error message "${error.message}" to include "${expectedError}"`,
              error.message,
              expectedError
            );
          } else if (expectedError instanceof RegExp && !expectedError.test(error.message)) {
            throw new AssertionError(
              `Expected thrown error message "${error.message}" to match regex ${expectedError}`,
              error.message,
              expectedError
            );
          }
        }
      }
    },

    toHaveProperty(prop, value) {
      const hasProp = actual !== null && typeof actual === 'object' && prop in actual;
      let pass = hasProp;
      if (pass && value !== undefined) {
        pass = deepEqual(actual[prop], value);
      }
      if (isNot ? pass : !pass) {
        throw new AssertionError(
          `Expected object ${isNot ? 'NOT ' : ''}to have property "${prop}"${value !== undefined ? ` with value ${JSON.stringify(value)}` : ''}`,
          actual,
          { [prop]: value }
        );
      }
    }
  });

  const base = matchers(false);
  base.not = matchers(true);
  return base;
}
