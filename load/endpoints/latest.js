import http from 'k6/http';
import { group } from 'k6';

import TestBase from '../base.js';
import { API_HOST, API_LATEST_LATENCY, API_LATEST_PATH } from '../constants.js';

export class FetchLatest extends TestBase {
    constructor() {
        super('LATEST', API_LATEST_LATENCY);
        this.URL = `${API_HOST}${API_LATEST_PATH}`;
        this.parameters = {
            sources: ['jhu', 'nyt'],
        };
    }

    test(trend) {
        group(this.testName, () => {
            const response = http.get(this._buildUrl());
            this.check(response, trend);
        });
    }

    _buildUrl() {
        return this.URL + this._addRandomParameters();
    }

    _addRandomParameters() {
        const source = this.chooseRandom(this.parameters.sources);
        return `?source=${source}`;
    }
}
