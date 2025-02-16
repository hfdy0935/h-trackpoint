const { getUserBaseInfo } = require('../lib/util/register');
const { UAParser } = require('ua-parser-js');

jest.mock('ua-parser-js');

describe('User Info Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('getUserBaseInfo', () => {
    test('should return user base info with new uid when not exists', async () => {
      const mockUAParser = {
        getBrowser: jest.fn().mockReturnValue({
          name: 'Chrome',
          version: '100.0.0'
        }),
        getOS: jest.fn().mockReturnValue({
          name: 'Windows',
          version: '10'
        }),
        getDevice: jest.fn().mockReturnValue({
          type: 'Desktop'
        })
      };

      (UAParser as jest.Mock).mockImplementation(() => mockUAParser);

      const result = await getUserBaseInfo();

      expect(result).toEqual({
        uid: expect.any(String),
        os: {
          name: 'Windows',
          version: '10'
        },
        device: 'Desktop',
        browser: {
          name: 'Chrome',
          version: '100.0.0'
        }
      });

      expect(localStorage.getItem('h-trackpoint-uid')).toBe(result.uid);
    });

    test('should return existing uid from localStorage', async () => {
      const existingUid = 'test-uid-123';
      localStorage.setItem('h-trackpoint-uid', existingUid);

      const mockUAParser = {
        getBrowser: jest.fn().mockReturnValue({
          name: 'Firefox',
          version: '90.0.0'
        }),
        getOS: jest.fn().mockReturnValue({
          name: 'Linux',
          version: '20.04'
        }),
        getDevice: jest.fn().mockReturnValue({
          type: 'Desktop'
        })
      };

      (UAParser as jest.Mock).mockImplementation(() => mockUAParser);

      const result = await getUserBaseInfo();

      expect(result.uid).toBe(existingUid);
      expect(result.browser.name).toBe('Firefox');
      expect(result.os.name).toBe('Linux');
    });

    test('should handle missing browser information', async () => {
      const mockUAParser = {
        getBrowser: jest.fn().mockReturnValue({}),
        getOS: jest.fn().mockReturnValue({
          name: 'Windows',
          version: '10'
        }),
        getDevice: jest.fn().mockReturnValue({
          type: null
        })
      };

      (UAParser as jest.Mock).mockImplementation(() => mockUAParser);

      const result = await getUserBaseInfo();

      expect(result.browser).toEqual({
        name: 'unknown',
        version: '0'
      });
      expect(result.device).toBeNull();
    });
  });
}); 