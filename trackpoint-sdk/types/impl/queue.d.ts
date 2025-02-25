import type { ISendEventParams } from '../type/event';
export declare class EventQueue {
    private queue;
    private processing;
    private maxRetries;
    private batchSize;
    private flushInterval;
    private retryInterval;
    private timer;
    constructor(config?: {
        maxRetries?: number;
        batchSize?: number;
        flushInterval?: number;
        retryInterval?: number;
    });
    enqueue(event: ISendEventParams): void;
    private processQueue;
    private startAutoFlush;
    destroy(): void;
}
