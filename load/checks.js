const API_WIDE_SLA = 5000;

export const apiChecks = {
    goodResponse: {
        "Response statuses should be 2xx (success)": response => [200, 201, 202, 203, 204].includes(response.status)
    },
    maximumLatency: {
        [`The API upholds an SLA of < ${API_WIDE_SLA}ms`]: response => response.timings.duration < API_WIDE_SLA
    },
    performance: (duration, response, threshold) => {
        // Check that the API performance (minus delay of server response) is not slowing down too much (10% buffer between full duration and wait time)
        const isWithinPerformanceBounds = response.timings.waiting < duration * 1.1;
        threshold.add(isWithinPerformanceBounds);

        return {
            [`Latest request had a server-side execution time of ${duration}. New executions should perform within 10% of this time.`]: () => isWithinPerformanceBounds
        };
    }
};