import { register } from '../lib/util/event-register';

describe('register', () => {
  let mockElement: HTMLElement;

  beforeEach(() => {
    mockElement = document.createElement('div');
    mockElement.id = 'test-element';
    document.body.appendChild(mockElement);
  });

  afterEach(() => {
    document.body.innerHTML = '';
    jest.clearAllMocks();
  });

  test('should register click event handler', () => {
    const mockCallback = jest.fn();
    register(mockElement, 'click', mockCallback);

    mockElement.click();
    expect(mockCallback).toHaveBeenCalledTimes(1);
    expect(mockCallback).toHaveBeenCalledWith({
      eventName: 'click',
      params: expect.objectContaining({
        elementId: 'test-element',
        elementTag: 'div',
        timestamp: expect.any(Number),
        url: expect.any(String),
        title: expect.any(String)
      })
    });
  });

  test('should register mouseover event handler', () => {
    const mockCallback = jest.fn();
    register(mockElement, 'mouseover', mockCallback);

    const mouseEvent = new MouseEvent('mouseover');
    mockElement.dispatchEvent(mouseEvent);

    expect(mockCallback).toHaveBeenCalledTimes(1);
    expect(mockCallback).toHaveBeenCalledWith({
      eventName: 'mouseover',
      params: expect.objectContaining({
        elementId: 'test-element',
        elementTag: 'div',
        timestamp: expect.any(Number),
        url: expect.any(String),
        title: expect.any(String)
      })
    });
  });

  test('should handle multiple event registrations on same element', () => {
    const mockClickCallback = jest.fn();
    const mockMouseoverCallback = jest.fn();

    register(mockElement, 'click', mockClickCallback);
    register(mockElement, 'mouseover', mockMouseoverCallback);

    mockElement.click();
    mockElement.dispatchEvent(new MouseEvent('mouseover'));

    expect(mockClickCallback).toHaveBeenCalledTimes(1);
    expect(mockMouseoverCallback).toHaveBeenCalledTimes(1);
  });
}); 