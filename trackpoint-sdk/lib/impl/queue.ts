import type { BatchEventItem, ISendEventParams } from "../type/event";
import { getCurrentTime } from "../util/request";
import { reqSendEvents } from "./http";

interface QueueItem {
  data: BatchEventItem;
  retryCount: number;
  timestamp: number;
}

export class EventQueue {
  private queue: QueueItem[] = [];
  private processing = false;
  private maxRetries: number = 3;
  private batchSize: number = 10;
  private flushInterval: number = 5000; // 5秒
  private retryInterval: number = 3000; // 3秒
  private timer: NodeJS.Timeout | null = null;

  constructor(config?: {
    maxRetries?: number;
    batchSize?: number;
    flushInterval?: number;
    retryInterval?: number;
  }) {
    if (config) {
      this.maxRetries = config.maxRetries ?? this.maxRetries;
      this.batchSize = config.batchSize ?? this.batchSize;
      this.flushInterval = config.flushInterval ?? this.flushInterval;
      this.retryInterval = config.retryInterval ?? this.retryInterval;
    }
    this.startAutoFlush();
  }

  public enqueue(event: ISendEventParams): void {
    this.queue.push({
      data: {
        eventName: event.eventName,
        params: event.params,
        pageUrl: window.location.href,
        createTime: getCurrentTime()
      },
      retryCount: 0,
      timestamp: Date.now(),
    });
    
    if (this.queue.length >= this.batchSize) {
      this.processQueue();
    }
  }

  private async processQueue(): Promise<void> {
    if (this.processing || this.queue.length === 0) {
      return;
    }

    this.processing = true;
    const batch = this.queue.splice(0, this.batchSize);

    try {
      await reqSendEvents(batch.map(item => item.data));
    } catch (error) {
      // 如果发送失败，将未超过重试次数的事件重新加入队列
      batch.forEach(item => {
        if (item.retryCount < this.maxRetries) {
          item.retryCount++;
          setTimeout(() => {
            this.queue.unshift(item);
          }, this.retryInterval);
        } else {
          console.error(`Failed to send event after ${this.maxRetries} retries:`, item.data);
        }
      });
    } finally {
      this.processing = false;
      if (this.queue.length >= this.batchSize) {
        this.processQueue();
      }
    }
  }

  private startAutoFlush(): void {
    this.timer = setInterval(() => {
      if (!this.processing && this.queue.length > 0) {
        this.processQueue();
      }
    }, this.flushInterval);
  }

  public destroy(): void {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    // 在销毁前尝试发送剩余的事件
    if (this.queue.length > 0) {
      this.processQueue();
    }
  }
}