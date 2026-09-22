/**
 * Simulated DOM & Browser Environment Shim for Scoreboard App E2E Tests
 * Provides standard DOM APIs, localStorage, IndexedDB, and touch/viewport simulations.
 */

class DOMTokenList {
  constructor(element) {
    this.element = element;
    this.tokens = new Set();
  }

  add(...classes) {
    for (const c of classes) {
      if (c) this.tokens.add(c);
    }
    this._sync();
  }

  remove(...classes) {
    for (const c of classes) {
      this.tokens.delete(c);
    }
    this._sync();
  }

  toggle(cls, force) {
    if (force !== undefined) {
      if (force) this.tokens.add(cls);
      else this.tokens.delete(cls);
    } else {
      if (this.tokens.has(cls)) this.tokens.delete(cls);
      else this.tokens.add(cls);
    }
    this._sync();
    return this.tokens.has(cls);
  }

  contains(cls) {
    return this.tokens.has(cls);
  }

  toString() {
    return Array.from(this.tokens).join(' ');
  }

  _sync() {
    this.element.attributes['class'] = this.toString();
  }
}

export class SimulatedElement {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.attributes = {};
    this.children = [];
    this.parentNode = null;
    this.style = {};
    this.classList = new DOMTokenList(this);
    this._textContent = '';
    this.listeners = new Map();
    this.rect = { top: 0, left: 0, width: 390, height: 844, bottom: 844, right: 390 };
  }

  get textContent() {
    if (this.children.length > 0) {
      return this.children.map(c => c.textContent).join('');
    }
    return this._textContent;
  }

  set textContent(val) {
    this.children = [];
    this._textContent = String(val);
  }

  get innerHTML() {
    return this.children.length > 0
      ? this.children.map(c => `<${c.tagName.toLowerCase()}>${c.innerHTML}</${c.tagName.toLowerCase()}>`).join('')
      : this._textContent;
  }

  set innerHTML(html) {
    this._textContent = String(html);
  }

  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === 'class') {
      this.classList.tokens.clear();
      for (const token of String(value).split(/\s+/).filter(Boolean)) {
        this.classList.tokens.add(token);
      }
    }
  }

  getAttribute(name) {
    return this.attributes[name] ?? null;
  }

  hasAttribute(name) {
    return name in this.attributes;
  }

  removeAttribute(name) {
    delete this.attributes[name];
    if (name === 'class') {
      this.classList.tokens.clear();
    }
  }

  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }

  removeChild(child) {
    const idx = this.children.indexOf(child);
    if (idx !== -1) {
      child.parentNode = null;
      this.children.splice(idx, 1);
    }
    return child;
  }

  addEventListener(event, listener) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(listener);
  }

  removeEventListener(event, listener) {
    if (!this.listeners.has(event)) return;
    const list = this.listeners.get(event).filter(l => l !== listener);
    this.listeners.set(event, list);
  }

  dispatchEvent(event) {
    event.target = this;
    const list = this.listeners.get(event.type) || [];
    for (const fn of list) {
      fn(event);
    }
    return !event.defaultPrevented;
  }

  getBoundingClientRect() {
    return { ...this.rect };
  }

  setBoundingClientRect(rect) {
    this.rect = { ...this.rect, ...rect };
  }

  querySelector(selector) {
    const all = this.querySelectorAll(selector);
    return all.length > 0 ? all[0] : null;
  }

  querySelectorAll(selector) {
    const results = [];
    const match = (el) => {
      if (selector.startsWith('#') && el.getAttribute('id') === selector.slice(1)) return true;
      if (selector.startsWith('.') && el.classList.contains(selector.slice(1))) return true;
      if (selector.startsWith('[') && selector.endsWith(']')) {
        const [attr, val] = selector.slice(1, -1).split('=');
        if (!val) return el.hasAttribute(attr);
        const cleanVal = val.replace(/['"]/g, '');
        return el.getAttribute(attr) === cleanVal;
      }
      if (el.tagName.toLowerCase() === selector.toLowerCase()) return true;
      return false;
    };

    const traverse = (el) => {
      for (const child of el.children) {
        if (match(child)) results.push(child);
        traverse(child);
      }
    };
    traverse(this);
    return results;
  }
}

export class SimulatedStorage {
  constructor() {
    this.store = new Map();
  }

  getItem(key) {
    return this.store.get(String(key)) ?? null;
  }

  setItem(key, val) {
    this.store.set(String(key), String(val));
  }

  removeItem(key) {
    this.store.delete(String(key));
  }

  clear() {
    this.store.clear();
  }

  get length() {
    return this.store.size;
  }

  key(n) {
    return Array.from(this.store.keys())[n] ?? null;
  }
}

export class SimulatedIndexedDB {
  constructor() {
    this.databases = new Map();
  }

  async openDB(name, version = 1, options = {}) {
    if (!this.databases.has(name)) {
      const db = {
        name,
        version,
        stores: new Map(),
      };
      this.databases.set(name, db);
      if (options.upgrade) {
        const upgradeDb = {
          createObjectStore: (storeName, storeOpts = {}) => {
            if (!db.stores.has(storeName)) {
              db.stores.set(storeName, {
                data: new Map(),
                keyPath: storeOpts.keyPath || 'id',
                autoIncrement: storeOpts.autoIncrement || false,
                indexes: new Map(),
              });
            }
            return {
              createIndex: (idxName, keyPath) => {
                db.stores.get(storeName).indexes.set(idxName, keyPath);
              },
            };
          },
        };
        await options.upgrade(upgradeDb, 0, version);
      }
    }

    const db = this.databases.get(name);

    return {
      get: async (storeName, key) => {
        const store = db.stores.get(storeName);
        if (!store) return undefined;
        return store.data.get(key);
      },

      put: async (storeName, val, key) => {
        const store = db.stores.get(storeName);
        if (!store) throw new Error(`Store ${storeName} not found`);
        const effectiveKey = key ?? (store.keyPath ? val[store.keyPath] : Date.now());
        store.data.set(effectiveKey, JSON.parse(JSON.stringify(val)));
        return effectiveKey;
      },

      delete: async (storeName, key) => {
        const store = db.stores.get(storeName);
        if (store) store.data.delete(key);
      },

      getAll: async (storeName) => {
        const store = db.stores.get(storeName);
        if (!store) return [];
        return Array.from(store.data.values()).map(v => JSON.parse(JSON.stringify(v)));
      },

      count: async (storeName) => {
        const store = db.stores.get(storeName);
        return store ? store.data.size : 0;
      },

      clear: async (storeName) => {
        const store = db.stores.get(storeName);
        if (store) store.data.clear();
      },

      close: () => {},
    };
  }

  reset() {
    this.databases.clear();
  }
}

export class EnvironmentShim {
  constructor() {
    this.reset();
  }

  reset() {
    this.document = {
      documentElement: new SimulatedElement('html'),
      body: new SimulatedElement('body'),
      createElement: (tag) => new SimulatedElement(tag),
      getElementById: (id) => this.document.body.querySelector(`#${id}`),
      querySelector: (sel) => this.document.body.querySelector(sel) || this.document.documentElement.querySelector(sel),
      querySelectorAll: (sel) => [
        ...this.document.documentElement.querySelectorAll(sel),
        ...this.document.body.querySelectorAll(sel),
      ],
    };

    this.localStorage = new SimulatedStorage();
    this.sessionStorage = new SimulatedStorage();
    this.indexedDB = new SimulatedIndexedDB();

    this.vibrateCalls = [];
    this.clipboardContent = '';

    this.navigator = {
      vibrate: (pattern) => {
        this.vibrateCalls.push(pattern);
        return true;
      },
      clipboard: {
        writeText: async (text) => {
          this.clipboardContent = String(text);
        },
        readText: async () => {
          return this.clipboardContent;
        },
      },
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148',
    };

    this.viewport = {
      width: 390,
      height: 844,
      scale: 1,
    };

    this.colorScheme = 'light';
    this.mediaListeners = [];

    this.window = {
      document: this.document,
      localStorage: this.localStorage,
      sessionStorage: this.sessionStorage,
      navigator: this.navigator,
      innerWidth: this.viewport.width,
      innerHeight: this.viewport.height,
      matchMedia: (query) => {
        const matches = query.includes('prefers-color-scheme: dark')
          ? this.colorScheme === 'dark'
          : query.includes('prefers-color-scheme: light')
          ? this.colorScheme === 'light'
          : false;

        return {
          matches,
          media: query,
          addEventListener: (evt, cb) => this.mediaListeners.push(cb),
          removeEventListener: (evt, cb) => {
            this.mediaListeners = this.mediaListeners.filter(l => l !== cb);
          },
        };
      },
      requestAnimationFrame: (cb) => setTimeout(cb, 16),
      cancelAnimationFrame: (id) => clearTimeout(id),
    };
  }

  setViewport(width, height) {
    this.viewport.width = width;
    this.viewport.height = height;
    this.window.innerWidth = width;
    this.window.innerHeight = height;
  }

  setColorScheme(scheme) {
    this.colorScheme = scheme;
    for (const listener of this.mediaListeners) {
      listener({ matches: scheme === 'dark' });
    }
  }

  applyGlobal() {
    if (typeof globalThis.document === 'undefined') {
      globalThis.document = this.document;
    }
    if (typeof globalThis.window === 'undefined') {
      globalThis.window = this.window;
    }
    if (typeof globalThis.localStorage === 'undefined') {
      globalThis.localStorage = this.localStorage;
    }
    if (typeof globalThis.navigator === 'undefined') {
      globalThis.navigator = this.navigator;
    }
  }
}

export const envShim = new EnvironmentShim();
