const jestDom = require('@testing-library/jest-dom');

// Mock window properties and methods that might not be available in jsdom
global.window.HTMLCanvasElement.prototype.getContext = () => ({});
global.window.HTMLCanvasElement.prototype.toDataURL = () => '';

// Mock crypto.randomUUID
Object.defineProperty(global, 'crypto', {
  value: {
    randomUUID: () => 'test-uuid-123'
  }
});

// Mock localStorage
Object.defineProperty(global, 'localStorage', {
  value: {
    store: {},
    getItem: function(key) {
      return this.store[key] || null;
    },
    setItem: function(key, value) {
      this.store[key] = value.toString();
    },
    clear: function() {
      this.store = {};
    }
  }
});

// Mock html2canvas
jest.mock('html2canvas', () => ({
  __esModule: true,
  default: jest.fn().mockResolvedValue({
    toDataURL: jest.fn().mockReturnValue('mock-image-data-url'),
  }),
})); 