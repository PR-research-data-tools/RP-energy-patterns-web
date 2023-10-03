// JavaScript Document

export class DynamicNudger {

	constructor(logger, maxRetries = 3, delay = 3000, dynamic = false) {
		this.maxRetries = maxRetries;
		this.maxDelay = 600000;
		this.delay = delay;
		this.dynamic = dynamic;
		this.logger = logger;
		this.logger.log("Nudger is ready...\n----");
	}
	
	fetchWithRetry(url) {
		return new Promise((resolve, reject) => {
			let retries = 0;

			const tryFetch = () => {
				this.logger.log(`Try to fetch, attempt #${retries}`);
				fetch(url)
					.then(response => {

						if (response.ok) {
							resolve(response);
						} else {
							if (retries < this.maxRetries) {
								let newDelay = this.delay;
								if (this.dynamic) {
									newDelay = Math.min(Math.pow(2.0, retries) * this.delay, this.maxDelay);
								}
								retries++;
								this.logger.log(`Request failed. Retrying in ${newDelay / 1000} seconds...`);
								setTimeout(tryFetch, newDelay);
							} else {
								reject(new Error(`Maximum retries exceeded. Unable to fetch ${url}`));
							}
						}
					})
					.catch(error => {
						this.logger.log("ERROR");
						if (retries < this.maxRetries) {
							let newDelay = this.delay;
								if (this.dynamic) {
									newDelay = Math.min(Math.pow(2.0, retries) * this.delay, this.maxDelay);
								}
							retries++;
							this.logger.log(`Request failed. Retrying in ${newDelay / 1000} seconds...`);
							setTimeout(tryFetch, newDelay);
						} else {
							reject(error);
						}
					});
			};

			tryFetch();
		});
	}

}
