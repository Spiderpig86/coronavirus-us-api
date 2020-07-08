import { group, fail, sleep } from 'k6';

import { FetchSources } from './endpoints/sources.js';
import { API_HOST, TEST_TPS_PER_USER } from './constants.js';

const testsToRun = [new FetchSources()];

export default () => {
    if (!API_HOST) {
        console.error('[ERROR] You must enter API_HOST variable when running k6 script with -e flag.');
        fail('Missing flag.');
    }
    
    if (!TEST_TPS_PER_USER === undefined) {
        console.error('[ERROR] You must enter TEST_TPS variable when running k6 script with -e flag.');
        fail('Missing flag.');
    }

    testsToRun.forEach(testClass => {
        group(testClass.testName, () => {
            testClass.test();
        });
    });
    
    if (TEST_TPS_PER_USER) {
        sleep(1.0 / Number(TEST_TPS_PER_USER));
    }
};
