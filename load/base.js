import { check } from 'k6';
import { Rate } from 'k6/metrics';

import { apiChecks } from './checks.js';

export default class TestBase {
    constructor(testName, lastDuration) {
        this.testName = testName;
        this.threshold = { [this.testName]: ['rate > 0.7'] };
        this.thresholdRate = new Rate(this.testName);
        this.lastDuration = lastDuration;
    }

    check(response) {
        check(response, 
            Object.assign(
                {},
                apiChecks.goodResponse,
                apiChecks.maximumLatency,
                apiChecks.performance(this.lastDuration, response, this.thresholdRate)
            ));
    }
}
