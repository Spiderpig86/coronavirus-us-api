export const TEST_TPS_PER_USER = __ENV.TEST_TPS;

export const SLOW_API_LATENCY = 15000;
export const AVERAGE_API_LATENCY = 1000;
export const FAST_API_LATENCY = 150;

export const API_HOST = __ENV.API_HOST;

export const API_SOURCES_PATH = '/api/data/sources';
export const API_SOURCES_LATENCY = FAST_API_LATENCY;
export const API_ALL_PATH = '/api/---/all';
export const API_ALL_LATENCY = SLOW_API_LATENCY;
export const API_LATEST_PATH = '/api/country/latest';
export const API_LATEST_LATENCY = FAST_API_LATENCY;

export const TEST_PASS_CRITERIA = 'rate > 0.7';
