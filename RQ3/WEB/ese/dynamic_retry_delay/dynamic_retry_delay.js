// JavaScript Document

import {Logger} from "../common/Logger.js";
import {DynamicNudger} from "./DynamicNudger.js";

function goForIt(maxRetries = 30, delay = 3000, dynamic = false) {
	// Do it
	const logger = new Logger("logger");
	logger.log("Logger is ready...");

	const url = "/ese/api/v1/nirwana";
	const nudger = new DynamicNudger(logger, maxRetries, delay, dynamic);
	
	nudger.fetchWithRetry(url)
		.then(response => {
			logger.log(`Successful response from ${url}:`, response);
		})
		.catch(error => {
			logger.log(`Failed to fetch ${url}:`, error);
		});

}

window.goForIt = goForIt;