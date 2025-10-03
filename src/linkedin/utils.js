/**
 * LinkedIn Automation Utilities
 *
 * Shared utility functions for LinkedIn automation scripts including element
 * detection, waiting, clicking, and text manipulation.
 *
 * @fileoverview Utility functions for LinkedIn automation
 * @author Your Name
 * @version 1.0.0
 */

/**
 * Extract text content from an element using XPath selector.
 *
 * @param {string} xpath - XPath selector for the target element
 * @returns {string} Trimmed text content or empty string if not found
 *
 * @example
 * const name = getTextByXpath("//h1[@class='profile-name']");
 * console.log(`Found name: ${name}`);
 */
function getTextByXpath(xpath) {
    const result = document.evaluate(
        xpath,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    );
    return result.singleNodeValue ? result.singleNodeValue.textContent.trim() : '';
}

/**
 * Check if an element exists using XPath selector and optionally match text content.
 *
 * @param {string} xpath - XPath selector for the element
 * @param {Object} [options={}] - Optional parameters
 * @param {string} [options.textToMatch] - Expected text content for validation
 * @returns {boolean} True if element exists (and text matches if specified)
 *
 * @example
 * // Check if Connect button exists
 * const hasConnectBtn = isElementPresentByXpath("//button[@class='connect']");
 *
 * // Check if button exists with specific text
 * const isPending = isElementPresentByXpath(
 *     "//button",
 *     { textToMatch: "Pending" }
 * );
 */
function isElementPresentByXpath(xpath, options = {}) {
    const result = document.evaluate(
        xpath,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    );
    const element = result.singleNodeValue;

    if (!element) {
        return false;
    }

    if ('textToMatch' in options && element.textContent.trim() !== options.textToMatch) {
        return false;
    }

    return true;
}

/**
 * Wait for an element to become visible and then click it.
 *
 * Polls the DOM at regular intervals until the element is found and visible,
 * then triggers a click event.
 *
 * @param {string} xpath - XPath selector for the element to click
 * @param {number} [maxWaitTime=5000] - Maximum time to wait in milliseconds
 * @returns {Promise<void>} Resolves when element is clicked or timeout occurs
 *
 * @example
 * // Click the Connect button when it becomes visible
 * await clickElementWhenVisible("//button[@class='connect-btn']", 10000);
 */
function clickElementWhenVisible(xpath, maxWaitTime = 5000) {
    const intervalTime = 100;
    let elapsedTime = 0;

    const intervalId = setInterval(() => {
        const result = document.evaluate(
            xpath,
            document,
            null,
            XPathResult.FIRST_ORDERED_NODE_TYPE,
            null
        );
        const element = result.singleNodeValue;

        // Check if element is found and visible
        if (element && element.offsetParent !== null) {
            clearInterval(intervalId);
            element.click();
            console.log("✓ Element clicked");
        } else {
            elapsedTime += intervalTime;
            if (elapsedTime >= maxWaitTime) {
                clearInterval(intervalId);
                console.log("⚠️  Timeout: Element not found or visible within max wait time");
            }
        }
    }, intervalTime);
}

/**
 * Wait for a text area to become visible and set its value.
 *
 * @param {string} xpath - XPath selector for the text area element
 * @param {string} text - Text content to set
 * @param {number} [maxWaitTime=5000] - Maximum time to wait in milliseconds
 * @returns {Promise<void>} Resolves when text is set or timeout occurs
 *
 * @example
 * const message = "Hi! I'd like to connect.";
 * await setTextWhenVisible("//textarea[@name='message']", message);
 */
function setTextWhenVisible(xpath, text, maxWaitTime = 5000) {
    const intervalTime = 100;
    let elapsedTime = 0;

    const intervalId = setInterval(() => {
        const result = document.evaluate(
            xpath,
            document,
            null,
            XPathResult.FIRST_ORDERED_NODE_TYPE,
            null
        );
        const textArea = result.singleNodeValue;

        if (textArea && textArea.offsetParent !== null) {
            clearInterval(intervalId);
            textArea.value = text;
            console.log("✓ Text set in text area");

            // Dispatch input event to trigger React/Vue updates
            const event = new Event('input', { bubbles: true });
            textArea.dispatchEvent(event);
            console.log("✓ Input event dispatched");
        } else {
            elapsedTime += intervalTime;
            if (elapsedTime >= maxWaitTime) {
                clearInterval(intervalId);
                console.log("⚠️  Timeout: Text area not found or visible");
            }
        }
    }, intervalTime);
}

/**
 * Wait for an element to appear in the DOM using CSS selector.
 *
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum time to wait in milliseconds
 * @returns {Promise<Element>} Promise that resolves with the found element
 * @throws {Error} If element is not found within timeout
 *
 * @example
 * try {
 *     const sendBtn = await waitForElement('.send-button', 5000);
 *     sendBtn.click();
 * } catch (error) {
 *     console.error('Send button not found:', error);
 * }
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
 * Wait for an element to become visible (not just present in DOM).
 *
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum time to wait in milliseconds
 * @returns {Promise<Element>} Promise that resolves with the visible element
 * @throws {Error} If element is not visible within timeout
 *
 * @example
 * const modal = await waitForElementVisible('.modal-dialog', 3000);
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
 * Wait for an element to become enabled (not disabled).
 *
 * @param {string} selector - CSS selector for the element
 * @param {number} [timeout=10000] - Maximum time to wait in milliseconds
 * @returns {Promise<Element>} Promise that resolves with the enabled element
 * @throws {Error} If element is not enabled within timeout
 *
 * @example
 * const submitBtn = await waitForElementEnabled('.submit-btn');
 * submitBtn.click();
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

/**
 * Trigger an input event on an element.
 *
 * Useful for notifying frameworks (React, Vue, Angular) that input value has changed.
 *
 * @param {Element} element - DOM element to trigger event on
 *
 * @example
 * const input = document.querySelector('input');
 * input.value = 'new value';
 * triggerInputEvent(input);
 */
function triggerInputEvent(element) {
    const event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });
    element.dispatchEvent(event);
}

/**
 * Generate a random delay between min and max values.
 *
 * @param {number} min - Minimum delay in milliseconds
 * @param {number} max - Maximum delay in milliseconds
 * @returns {number} Random delay value
 *
 * @example
 * const delay = getRandomDelay(2000, 5000);
 * await new Promise(resolve => setTimeout(resolve, delay));
 */
function getRandomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Export utilities for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getTextByXpath,
        isElementPresentByXpath,
        clickElementWhenVisible,
        setTextWhenVisible,
        waitForElement,
        waitForElementVisible,
        waitForElementEnabled,
        triggerInputEvent,
        getRandomDelay
    };
}
