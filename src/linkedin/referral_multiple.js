/**
 * LinkedIn Mass Referral Automation
 *
 * Automates sending connection requests with personalized messages to multiple
 * LinkedIn profiles on a company's People page. Includes rate limiting, error
 * handling, and safety features to avoid LinkedIn restrictions.
 *
 * @fileoverview Bulk LinkedIn connection request automation with personalization
 * @author Your Name
 * @version 2.0.0
 *
 * @usage
 * 1. Navigate to a company's LinkedIn People page
 * 2. Apply filters (location, position, etc.)
 * 3. Open browser DevTools console
 * 4. Paste and run this script
 * 5. Enter company name and optional job ID when prompted
 *
 * @warning
 * - Use responsibly to avoid LinkedIn account restrictions
 * - Limit bulk actions to 10-20 connections per session
 * - Wait 24-48 hours between automation sessions
 * - LinkedIn's terms of service prohibit automation
 */

/**
 * Prompt user for company name and job ID, then initiate bulk outreach.
 *
 * @returns {void}
 *
 * @example
 * // User will be prompted for:
 * // - Company name (e.g., "Microsoft")
 * // - Job ID (optional, e.g., "JOB-12345")
 */
function askForCompanyName() {
    const companyName = prompt("Please enter the name of the company:");
    const jobId = prompt("Please enter the job id of the position (or leave blank): ");

    if (companyName) {
        if (jobId) {
            clickConnectAndSendNote(companyName, 20, { jobId: jobId });
        } else {
            clickConnectAndSendNote(companyName, 20);
        }
    } else {
        console.log("⚠️  No company name provided. Operation cancelled.");
    }
}

/**
 * Simulate a middle mouse button click event.
 *
 * Useful for opening links in new tabs without changing focus.
 *
 * @param {Element} element - DOM element to click
 * @returns {void}
 */
function simulateMiddleClick(element) {
    const event = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
        button: 1  // Middle mouse button
    });
    element.dispatchEvent(event);
}

/**
 * Send connection requests with personalized notes to multiple profiles.
 *
 * This is the main automation function that iterates through profile cards
 * on a company's People page, sends connection requests with personalized
 * messages, and handles various edge cases and errors.
 *
 * @async
 * @param {string} companyName - Name of the company for personalization
 * @param {number} [limit=20] - Maximum number of connection requests to send
 * @param {Object} [options={}] - Optional parameters
 * @param {string} [options.jobId] - Specific job ID to mention in message
 * @returns {Promise<void>}
 *
 * @example
 * // Send 15 connection requests mentioning a specific job
 * await clickConnectAndSendNote("Microsoft", 15, { jobId: "JOB-12345" });
 *
 * @example
 * // Send 10 general connection requests
 * await clickConnectAndSendNote("Google", 10);
 */
async function clickConnectAndSendNote(companyName, limit = 20, options = {}) {
    const profileCards = document.querySelectorAll('.org-people-profile-card');
    let processedCount = 0;
    const randomDelay = Math.floor(Math.random() * (45000 - 30000 + 1)) + 30000;

    console.log(`\ud83d\ude80 Starting outreach campaign for ${companyName}`);
    console.log(`   Target: ${limit} connections with ${randomDelay/1000}s delay between each`);

    for (const card of profileCards) {
        if (processedCount >= limit) {
            console.log(`\u2705 Reached limit of ${limit} connections`);
            break;
        }

        const connectButton = card.querySelector('button[aria-label^="Invite"]');
        const nameElement = card.querySelector('.org-people-profile-card__profile-info .lt-line-clamp--single-line');

        // Skip if button is "Message" (already connected)
        if (!connectButton || connectButton.textContent.trim() === "Message") {
            if (nameElement) {
                console.log(`\ud83d\udd17 Already connected to ${nameElement.textContent.trim()}, skipping...`);
            }
            continue;
        }

        // Skip if no name element found
        if (!nameElement) {
            console.log("\u26a0\ufe0f  Couldn't find name element, skipping...");
            continue;
        }

        // Skip LinkedIn Member placeholders
        if (nameElement.textContent.trim() === "LinkedIn Member") {
            console.log("\u26a0\ufe0f  LinkedIn Member placeholder detected, skipping...");
            continue;
        }

        // Skip if connection already pending
        if (connectButton.textContent.trim() === "Pending") {
            console.log(`\u23f3 Request already pending for ${nameElement.textContent.trim()}, skipping...`);
            continue;
        }

        const firstName = nameElement.textContent.trim().split(" ")[0] || "there";

        // Generate personalized message
        let message = '';
        if ("jobId" in options) {
            message = `Hi ${firstName}! I'm looking to apply for an SDE role (Job ID: ${options.jobId}) at ${companyName}. Would you be willing to look at my resume or reach out to me if you need any additional information? Thanks!`;
        } else {
            message = `Hi ${firstName}! I'm looking to apply for an SDE role at ${companyName}. Would you be willing to look at my resume or reach out to me if you need any additional information? Thanks!`;
        }

        console.log(`\ud83d\udcac Preparing message for ${firstName}: "${message.substring(0, 50)}..."`);

        // Click the Connect button
        connectButton.click();

        try {
            // Check if email is required (skip these profiles)
            const emailLabel = await waitForElementVisible('label[for="email"]', 2000)
                .catch(() => null);

            if (emailLabel) {
                console.log(`\u26a0\ufe0f  Email required for ${firstName}, skipping...`);
                document.querySelector('button[aria-label="Dismiss"]').click();
                await new Promise(resolve => setTimeout(resolve, randomDelay));
                continue;
            }

            // Wait for and click "Add a note" button
            await waitForElement('.artdeco-button[aria-label="Add a note"]');
            document.querySelector('.artdeco-button[aria-label="Add a note"]').click();

            // Enter the personalized message
            await waitForElement('textarea[name="message"]');
            const textArea = document.querySelector('textarea[name="message"]');
            textArea.value = message;
            triggerInputEvent(textArea);

            // Wait for "Send now" button and click it
            await waitForElementEnabled('.artdeco-button[aria-label="Send now"]');
            document.querySelector('.artdeco-button[aria-label="Send now"]').click();

            processedCount++;
            console.log(`\u2705 [${processedCount}/${limit}] Connection request sent to ${firstName}`);

        } catch (error) {
            console.error(`\u274c Error processing ${firstName}:`, error.message);
            continue;
        }

        // Wait before processing next profile
        console.log(`\u23f1\ufe0f  Waiting ${randomDelay/1000}s before next request...`);
        await new Promise(resolve => setTimeout(resolve, randomDelay));
    }

    console.log(`\n\ud83c\udf89 Campaign complete! Sent ${processedCount} connection requests.`);
}

/**
 * Wait for an element to become visible in the DOM.
 *
 * @async
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum wait time in milliseconds
 * @returns {Promise<Element>} Promise resolving to the visible element
 * @throws {Error} If element not visible within timeout
 */
function waitForElementVisible(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element && element.offsetWidth > 0 && element.offsetHeight > 0) {
                clearInterval(interval);
                resolve(element);
            }
        }, 500);

        setTimeout(() => {
            clearInterval(interval);
            reject(new Error(`Element "${selector}" not visible within ${timeout}ms`));
        }, timeout);
    });
}

/**
 * Wait for an element to appear in the DOM.
 *
 * @async
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum wait time in milliseconds
 * @returns {Promise<Element>} Promise resolving to the found element
 * @throws {Error} If element not found within timeout
 */
function waitForElement(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(interval);
                resolve(element);
            }
        }, 500);

        setTimeout(() => {
            clearInterval(interval);
            reject(new Error(`Element "${selector}" not found within ${timeout}ms`));
        }, timeout);
    });
}

/**
 * Trigger an input event on an element.
 *
 * @param {Element} element - DOM element to dispatch event on
 * @returns {void}
 */
function triggerInputEvent(element) {
    const event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });
    element.dispatchEvent(event);
}

/**
 * Wait for an element to become enabled.
 *
 * @async
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum wait time in milliseconds
 * @returns {Promise<Element>} Promise resolving to the enabled element
 * @throws {Error} If element not enabled within timeout
 */
function waitForElementEnabled(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element && !element.disabled) {
                clearInterval(interval);
                resolve(element);
            }
        }, 500);

        setTimeout(() => {
            clearInterval(interval);
            reject(new Error(`Element "${selector}" not enabled within ${timeout}ms`));
        }, timeout);
    });
}

// Start the automation
askForCompanyName();
