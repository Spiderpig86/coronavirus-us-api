import { check } from 'k6';
import { Rate } from 'k6/metrics';

import { apiChecks } from './checks.js';
import { TEST_PASS_CRITERIA } from './constants.js';

export default class TestBase {
    constructor(testName, lastDuration) {
        this.testName = testName;
        this.threshold = { [this.testName]: [TEST_PASS_CRITERIA] };
        this.thresholdRate = new Rate(this.testName);
        this.lastDuration = lastDuration; // Jitter
    }

    check(response, trend) {
        trend.add(response.timings.waiting);
        this.lastDuration = response.timings.waiting;
        check(
            response,
            Object.assign(
                {},
                apiChecks.goodResponse,
                apiChecks.maximumLatency,
                apiChecks.performance(this.lastDuration, response, this.thresholdRate)
            )
        );
    }

    chooseRandom(collection) {
        return collection[Math.floor(Math.random() * collection.length)];
    }
}
