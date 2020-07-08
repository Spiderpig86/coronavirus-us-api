import http from 'k6/http';
import { group } from 'k6';

import TestBase from '../base.js';
import { API_HOST, API_SOURCES_LATENCY, API_SOURCES_PATH } from '../constants.js';

export class FetchSources extends TestBase {
    constructor() {
        super("DATA", API_SOURCES_LATENCY);
        this.URL = `${API_HOST}${API_SOURCES_PATH}`;
    }

    test() {
        group(this.testName, () => {
            const response = http.get(this.URL);
            this.check(response);
        });
    }
}
