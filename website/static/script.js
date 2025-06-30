// Schizophrenia Prediction Website - JavaScript Functions

class SchizophreniaPrediction {
	constructor() {
		this.form = document.getElementById("predictionForm");
		this.resultsDiv = document.getElementById("results");
		this.init();
	}

	init() {
		if (this.form) {
			this.form.addEventListener("submit", this.handleSubmit.bind(this));
			this.setupFormValidation();
			this.setupTooltips();
		}
	}

	setupFormValidation() {
		const inputs = this.form.querySelectorAll('input[type="number"]');
		inputs.forEach(input => {
			input.addEventListener("input", this.validateInput.bind(this));
			input.addEventListener("blur", this.validateInput.bind(this));
		});
	}

	validateInput(event) {
		const input = event.target;
		const value = parseFloat(input.value);
		const min = parseFloat(input.getAttribute("min"));
		const max = parseFloat(input.getAttribute("max"));

		// Remove previous validation classes
		input.classList.remove("is-valid", "is-invalid");

		if (isNaN(value)) {
			return; // Empty input, let HTML5 validation handle required fields
		}

		if (value < min || value > max) {
			input.classList.add("is-invalid");
			this.showInputError(input, `Value must be between ${min} and ${max}`);
		} else {
			input.classList.add("is-valid");
			this.hideInputError(input);
		}
	}

	showInputError(input, message) {
		let errorDiv = input.parentNode.querySelector(".invalid-feedback");
		if (!errorDiv) {
			errorDiv = document.createElement("div");
			errorDiv.className = "invalid-feedback";
			input.parentNode.appendChild(errorDiv);
		}
		errorDiv.textContent = message;
	}

	hideInputError(input) {
		const errorDiv = input.parentNode.querySelector(".invalid-feedback");
		if (errorDiv) {
			errorDiv.remove();
		}
	}

	setupTooltips() {
		// Initialize Bootstrap tooltips
		const tooltipTriggerList = [].slice.call(
			document.querySelectorAll('[data-bs-toggle="tooltip"]')
		);
		tooltipTriggerList.map(function(tooltipTriggerEl) {
			return new bootstrap.Tooltip(tooltipTriggerEl);
		});
	}

	async handleSubmit(event) {
		event.preventDefault();

		// Validate form before submission
		if (!this.validateForm()) {
			return;
		}

		const submitBtn = this.form.querySelector('button[type="submit"]');
		const loading = submitBtn.querySelector(".loading");
		const btnText = submitBtn.querySelector(".btn-text");

		try {
			// Show loading state
			this.setLoadingState(true, submitBtn, loading, btnText);

			// Hide previous results
			if (this.resultsDiv) {
				this.resultsDiv.style.display = "none";
			}

			// Prepare form data
			const formData = new FormData(this.form);

			// Make prediction request
			const response = await fetch("/predict", {
				method: "POST",
				body: formData
			});

			const data = await response.json();

			if (data.success) {
				this.showResults(data.prediction, data.probabilities);
				this.trackPrediction(data); // Analytics
			} else {
				this.showError(data.error);
			}
		} catch (error) {
			console.error("Prediction error:", error);
			this.showError(
				"Network error occurred. Please check your connection and try again."
			);
		} finally {
			// Hide loading state
			this.setLoadingState(false, submitBtn, loading, btnText);
		}
	}

	validateForm() {
		const requiredInputs = this.form.querySelectorAll(
			"input[required], select[required]"
		);
		let isValid = true;

		requiredInputs.forEach(input => {
			if (!input.value.trim()) {
				input.classList.add("is-invalid");
				this.showInputError(input, "This field is required");
				isValid = false;
			}
		});

		return isValid;
	}

	setLoadingState(loading, submitBtn, loadingElement, btnTextElement) {
		if (loading) {
			loadingElement.style.display = "inline";
			btnTextElement.style.display = "none";
			submitBtn.disabled = true;
		} else {
			loadingElement.style.display = "none";
			btnTextElement.style.display = "inline";
			submitBtn.disabled = false;
		}
	}

	showResults(prediction, probabilities) {
		if (!this.resultsDiv) return;

		const predictionDiv = document.getElementById("prediction-result");
		const probabilitiesDiv = document.getElementById("probabilities-result");

		// Show main prediction
		this.renderPrediction(predictionDiv, prediction);

		// Show probabilities
		this.renderProbabilities(probabilitiesDiv, probabilities);

		// Show results with animation
		this.resultsDiv.style.display = "block";
		this.resultsDiv.classList.add("fade-in-up");

		// Scroll to results
		setTimeout(() => {
			this.resultsDiv.scrollIntoView({
				behavior: "smooth",
				block: "start"
			});
		}, 100);
	}

	renderPrediction(container, prediction) {
		const riskConfig = this.getRiskConfiguration(prediction);

		container.innerHTML = `
            <div class="prediction-result ${riskConfig.class}">
                <div class="d-flex align-items-center justify-content-center mb-3">
                    <div class="icon-circle" style="background: rgba(255,255,255,0.2);">
                        <i class="${riskConfig.icon}"></i>
                    </div>
                    <div>
                        <h3 class="mb-1">Predicted Risk Level</h3>
                        <h2 class="mb-0 fw-bold">${prediction}</h2>
                    </div>
                </div>
                <p class="mb-0 text-center">
                    ${riskConfig.description}
                </p>
            </div>
        `;
	}

	renderProbabilities(container, probabilities) {
		// Sort probabilities by value (descending)
		const sortedProbs = Object.entries(probabilities).sort(
			(a, b) => b[1] - a[1]
		);

		let html =
			'<h5 class="mb-4"><i class="fas fa-chart-bar me-2"></i>Probability Distribution</h5>';

		sortedProbs.forEach(([className, probability]) => {
			const riskConfig = this.getRiskConfiguration(className);
			const barClass = this.getProbabilityBarClass(className);

			html += `
                <div class="mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="fw-medium">
                            <i class="${riskConfig.icon} me-2"></i>
                            ${className}
                        </span>
                        <span class="fw-bold">${probability}%</span>
                    </div>
                    <div class="probability-bar">
                        <div class="probability-fill ${barClass}" 
                             style="width: ${probability}%">
                            ${probability > 20 ? probability + "%" : ""}
                        </div>
                    </div>
                </div>
            `;
		});

		container.innerHTML = html;

		// Animate probability bars
		setTimeout(() => {
			const bars = container.querySelectorAll(".probability-fill");
			bars.forEach(bar => {
				const width = bar.style.width;
				bar.style.width = "0%";
				setTimeout(() => {
					bar.style.width = width;
				}, 100);
			});
		}, 100);
	}

	getRiskConfiguration(riskLevel) {
		const configs = {
			"High Proneness": {
				class: "risk-high",
				icon: "fas fa-exclamation-circle",
				description:
					"High risk level detected. Immediate professional consultation is strongly recommended."
			},
			"Elevated Proneness": {
				class: "risk-elevated",
				icon: "fas fa-exclamation-triangle",
				description:
					"Elevated risk level detected. Professional monitoring and evaluation recommended."
			},
			"Moderate Proneness": {
				class: "risk-moderate",
				icon: "fas fa-minus-circle",
				description:
					"Moderate risk level detected. Regular monitoring may be beneficial."
			},
			"Low Proneness": {
				class: "risk-low",
				icon: "fas fa-check-circle",
				description:
					"Low risk level detected. Continue regular health monitoring."
			},
			"Minimal Proneness": {
				class: "risk-minimal",
				icon: "fas fa-shield-alt",
				description:
					"Minimal risk level detected. Maintain current health practices."
			}
		};

		return configs[riskLevel] || configs["Moderate Proneness"];
	}

	getProbabilityBarClass(riskLevel) {
		const classes = {
			"High Proneness": "bg-danger",
			"Elevated Proneness": "bg-warning",
			"Moderate Proneness": "bg-info",
			"Low Proneness": "bg-primary",
			"Minimal Proneness": "bg-success"
		};

		return classes[riskLevel] || "bg-secondary";
	}

	showError(errorMessage) {
		if (!this.resultsDiv) return;

		const predictionDiv = document.getElementById("prediction-result");
		const probabilitiesDiv = document.getElementById("probabilities-result");

		predictionDiv.innerHTML = `
            <div class="alert alert-danger-custom alert-custom">
                <div class="d-flex align-items-center">
                    <i class="fas fa-exclamation-triangle fa-2x me-3"></i>
                    <div>
                        <h5 class="mb-1">Prediction Error</h5>
                        <p class="mb-0">${errorMessage}</p>
                    </div>
                </div>
            </div>
        `;

		probabilitiesDiv.innerHTML = "";
		this.resultsDiv.style.display = "block";
	}

	trackPrediction(data) {
		// Analytics tracking (if needed)
		if (typeof gtag !== "undefined") {
			gtag("event", "prediction_made", {
				event_category: "ML_Model",
				event_label: data.prediction,
				value: Math.round(Math.max(...Object.values(data.probabilities)))
			});
		}
	}

	// Utility method to reset form
	resetForm() {
		this.form.reset();
		this.form.querySelectorAll(".is-valid, .is-invalid").forEach(input => {
			input.classList.remove("is-valid", "is-invalid");
		});
		this.form.querySelectorAll(".invalid-feedback").forEach(error => {
			error.remove();
		});
		if (this.resultsDiv) {
			this.resultsDiv.style.display = "none";
		}
	}

	// Method to prefill form with sample data
	fillSampleData(sampleType = "moderate") {
		const samples = {
			moderate: {
				age: 68,
				gender: 0,
				marital_status: 2,
				fatigue: 0.3,
				slowing: 0.2,
				pain: 0.1,
				hygiene: 0.4,
				movement: 0.3
			},
			high: {
				age: 75,
				gender: 1,
				marital_status: 3,
				fatigue: 0.8,
				slowing: 0.7,
				pain: 0.6,
				hygiene: 0.2,
				movement: 0.9
			},
			low: {
				age: 60,
				gender: 0,
				marital_status: 1,
				fatigue: 0.1,
				slowing: 0.1,
				pain: 0.0,
				hygiene: 0.8,
				movement: 0.2
			}
		};

		const sample = samples[sampleType] || samples.moderate;

		Object.keys(sample).forEach(key => {
			const input = this.form.querySelector(`[name="${key}"]`);
			if (input) {
				input.value = sample[key];
				input.dispatchEvent(new Event("input"));
			}
		});
	}
}

// Utility functions
function copyResultsToClipboard() {
	const resultsDiv = document.getElementById("results");
	if (!resultsDiv || resultsDiv.style.display === "none") {
		alert("No results to copy");
		return;
	}

	const predictionText = resultsDiv.querySelector(".prediction-result h2")
		.textContent;
	const probabilities = Array.from(
		resultsDiv.querySelectorAll(".probability-bar")
	)
		.map(bar => {
			const label = bar.previousElementSibling
				.querySelector("span")
				.textContent.trim();
			const percentage = bar.previousElementSibling.querySelector(".fw-bold")
				.textContent;
			return `${label}: ${percentage}`;
		})
		.join("\n");

	const textToCopy = `Schizophrenia Risk Prediction\n\nPredicted Level: ${predictionText}\n\nProbabilities:\n${probabilities}\n\nGenerated by Schizophrenia Prediction System`;

	navigator.clipboard
		.writeText(textToCopy)
		.then(() => {
			// Show success message
			const toast = document.createElement("div");
			toast.className =
				"alert alert-success-custom alert-custom position-fixed";
			toast.style.cssText =
				"top: 20px; right: 20px; z-index: 10000; min-width: 300px;";
			toast.innerHTML =
				'<i class="fas fa-check-circle me-2"></i>Results copied to clipboard!';
			document.body.appendChild(toast);

			setTimeout(() => {
				document.body.removeChild(toast);
			}, 3000);
		})
		.catch(err => {
			console.error("Failed to copy to clipboard:", err);
			alert("Failed to copy results to clipboard");
		});
}

// Initialize the application when DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
	// Initialize the main prediction app
	window.predictionApp = new SchizophreniaPrediction();

	// Add sample data buttons (for testing)
	if (document.getElementById("predictionForm")) {
		const form = document.getElementById("predictionForm");
		const buttonsContainer = document.createElement("div");
		buttonsContainer.className = "text-center mt-3";
		buttonsContainer.innerHTML = `
            <small class="text-muted d-block mb-2">Quick Test Data:</small>
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-secondary" onclick="predictionApp.fillSampleData('low')">
                    Low Risk Sample
                </button>
                <button type="button" class="btn btn-outline-secondary" onclick="predictionApp.fillSampleData('moderate')">
                    Moderate Risk Sample
                </button>
                <button type="button" class="btn btn-outline-secondary" onclick="predictionApp.fillSampleData('high')">
                    High Risk Sample
                </button>
            </div>
        `;
		form.appendChild(buttonsContainer);
	}

	// Initialize other page-specific features
	initializePageFeatures();
});

function initializePageFeatures() {
	// Smooth scrolling for anchor links
	document.querySelectorAll('a[href^="#"]').forEach(anchor => {
		anchor.addEventListener("click", function(e) {
			e.preventDefault();
			const target = document.querySelector(this.getAttribute("href"));
			if (target) {
				target.scrollIntoView({
					behavior: "smooth"
				});
			}
		});
	});

	// Add fade-in animation to cards
	const cards = document.querySelectorAll(".card");
	const observer = new IntersectionObserver(entries => {
		entries.forEach(entry => {
			if (entry.isIntersecting) {
				entry.target.classList.add("fade-in-up");
			}
		});
	});

	cards.forEach(card => {
		observer.observe(card);
	});
}
