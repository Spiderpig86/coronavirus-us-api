import { group, fail, sleep } from 'k6';
import { Trend } from 'k6/metrics';

import { FetchSources } from './endpoints/sources.js';
import { FetchAll } from './endpoints/all.js';
import { FetchLatest } from './endpoints/latest.js';
import { API_HOST, TEST_TPS_PER_USER } from './constants.js';

const testsToRun = [
    { endpoint: new FetchSources(), trend: new Trend('SOURCES_LATENCY') },
    { endpoint: new FetchAll(), trend: new Trend('ALL_LATENCY') },
    { endpoint: new FetchLatest(), trend: new Trend('LATEST_LATENCY') },
];

export default () => {
    if (!API_HOST) {
        console.error('[ERROR] You must enter API_HOST variable when running k6 script with -e flag.');
        fail('Missing flag.');
    }

    if (!TEST_TPS_PER_USER === undefined) {
        console.error('[ERROR] You must enter TEST_TPS variable when running k6 script with -e flag.');
        fail('Missing flag.');
    }

    testsToRun.forEach((test) => {
        group(test.endpoint.testName, () => {
            test.endpoint.test(test.trend);
        });
    });

    if (TEST_TPS_PER_USER) {
        sleep(1.0 / Number(TEST_TPS_PER_USER));
    }
};
