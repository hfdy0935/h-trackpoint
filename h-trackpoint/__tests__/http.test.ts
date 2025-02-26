import { reqSendEvents, reqRegister, reqSendScreenshot } from '../lib/impl/http';
import html2canvas from 'html2canvas';

jest.mock('html2canvas');
jest.mock('../lib/util/request', () => ({
  request: {
    post: jest.fn()
  }
}));

import { request } from '../lib/util/request';

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
      os: {
        name: 'Windows',
        version: '1.1.1'
      },
      device: 'mobile' as const,
      browser: {
        name: 'Chrome',
        version: '1.1.1'
      }
    };

    test('should register successfully', async () => {
      const mockResponse = {
        data: {
          code: 200,
          data: ['CLICK', 'MOUSEOVER'],
          msg: 'success'
        }
      };
      // @ts-ignore
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
      // @ts-ignore
      request.post.mockResolvedValueOnce(mockResponse);

      const result = await reqSendEvents(mockEventData);
      expect(result.data.code).toBe(200);
      expect(result.data.data?.[0].record_id).toBe('test-record');
    });

    test('should handle send failure gracefully', async () => {
      // @ts-ignore
      request.post.mockRejectedValueOnce(new Error('Network error'));
      await expect(reqSendEvents(mockEventData)).rejects.toThrow('Network error');
    });
  });
  describe('reqSendScreenshot', () => {
    const mockRids = ['record-id-1', 'record-id-2'];

    test('should send screenshot successfully', async () => {
      // 创建一个模拟的 canvas 对象
      const mockCanvas = {
        toBlob: jest.fn((callback: (blob: Blob | null) => void) => {
          const mockBlob = new Blob(['mock screenshot'], { type: 'image/png' });
          callback(mockBlob);
        })
      };

      // 模拟 html2canvas 返回 mockCanvas
      (html2canvas as jest.Mock).mockResolvedValueOnce(mockCanvas);

      // 模拟 request.post 返回成功响应
      const mockResponse = {
        data: {
          code: 200,
          msg: 'success'
        }
      };
      // @ts-ignore
      request.post.mockResolvedValueOnce(mockResponse);

      await reqSendScreenshot(mockRids);

      // 断言 html2canvas 被调用
      expect(html2canvas).toHaveBeenCalledWith(document.documentElement);

      // 断言 toBlob 被调用
      expect(mockCanvas.toBlob).toHaveBeenCalled();

      // 断言 request.post 被调用
      expect(request.post).toHaveBeenCalledWith('/upload-shot', expect.any(FormData));

      // 获取传递给 request.post 的 FormData
      const formData = (request.post as jest.Mock).mock.calls[0][1];

      // 断言 FormData 包含正确的数据
      expect(formData.get('screenshot')).toBeInstanceOf(Blob);
      expect(formData.getAll('record_id_list')).toEqual(mockRids);
    });
  });
}); 