// JavaScript Document

export class Logger {

	constructor(id) {
		this.container = document.getElementById(id);;
	}

	log(message) {
		const entry = document.createElement('div');
		entry.classList.add("log-entry");
		entry.innerText = message;
		this.container.appendChild(entry);
	}
}
