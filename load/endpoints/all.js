import http from 'k6/http';
import { group } from 'k6';

import TestBase from '../base.js';
import { API_HOST, API_ALL_LATENCY, API_ALL_PATH } from '../constants.js';

export class FetchAll extends TestBase {
    constructor() {
        super('ALL', API_ALL_LATENCY);
        this.URL = `${API_HOST}${API_ALL_PATH}`;
        this.parameters = {
            paths: ['county', 'state', 'country'],
            sources: ['jhu', 'nyt'],
            options: ['timelines', 'properties'],
        };
    }

    test(trend) {
        group(this.testName, () => {
            const response = http.get(this._buildUrl());
            this.check(response, trend);
        });
    }

    _buildUrl() {
        const url = this.URL.replace('---', this.parameters.paths[Math.floor(Math.random() * this.parameters.paths.length)]);
        
        return url + this._addRandomParameters();
    }

    _addRandomParameters() {
        const querySet = new Set();
        const source = this.chooseRandom(this.parameters.sources);

        const numParameters = Math.floor(Math.random() * (this.parameters.options.length + 1));

        for (let i = 0; i < numParameters; i++) {
            querySet.add(this.chooseRandom(this.parameters.options));
        }

        return `?source=${source}` + [...querySet].reduce((acc, cur) => acc + `&${cur}=true`, '');
    }
}
