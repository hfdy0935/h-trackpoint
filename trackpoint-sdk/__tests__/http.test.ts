const { reqSendEvents, reqRegister } = require('../lib/impl/http');

jest.mock('../lib/util/request', () => ({
  request: {
    post: jest.fn()
  }
}));

const { request } = require('../lib/util/request');

describe('HTTP Implementation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('reqRegister', () => {
    const mockOptions = {
      projectId: 'test-project',
      projectKey: 'test-key',
      uploadPercent: 1,
      maxRetries: 3,
      batchSize: 10,
      flushInterval: 5000,
      retryInterval: 3000,
    };

    const mockBaseInfo = {
      uid: 'test-user',
      os: 'Windows',
      device: 'Desktop',
      browser: 'Chrome'
    };

    test('should register successfully', async () => {
      const mockResponse = {
        data: {
          code: 200,
          data: ['CLICK', 'MOUSEOVER'],
          msg: 'success'
        }
      };

      request.post.mockResolvedValueOnce(mockResponse);

      const result = await reqRegister(mockOptions, mockBaseInfo);
      expect(result.data.code).toBe(200);
      expect(result.data.data).toEqual(['CLICK', 'MOUSEOVER']);
    });
  });

  describe('reqSendEvents', () => {
    const mockEventData = {
      uid: 'test-user',
      projectId: 'test-project',
      projectKey: 'test-key',
      events: [{
        eventName: 'click',
        params: { elementId: 'test-button' },
        pageUrl: 'http://test.com',
        createTime: Date.now()
      }]
    };

    test('should send events successfully', async () => {
      const mockResponse = {
        data: {
          code: 200,
          data: [{
            record_id: 'test-record',
            need_upload_shot: false
          }],
          msg: 'success'
        }
      };

      request.post.mockResolvedValueOnce(mockResponse);

      const result = await reqSendEvents(mockEventData);
      expect(result.data.code).toBe(200);
      expect(result.data.data[0].record_id).toBe('test-record');
    });

    test('should handle send failure gracefully', async () => {
      request.post.mockRejectedValueOnce(new Error('Network error'));
      await expect(reqSendEvents(mockEventData)).rejects.toThrow('Network error');
    });
  });
}); 