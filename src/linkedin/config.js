/**
 * LinkedIn Automation Configuration
 *
 * Shared configuration for LinkedIn automation scripts including XPath selectors,
 * CSS selectors, timing constants, and utility functions.
 *
 * @fileoverview Configuration and shared utilities for LinkedIn automation
 * @author Your Name
 * @version 1.0.0
 */

/**
 * XPath selectors for LinkedIn profile elements.
 * These selectors are used to locate specific elements on LinkedIn pages.
 *
 * @constant {Object} XPATHS
 * @property {string} name - XPath for primary name element
 * @property {string} name2 - XPath for alternative name element location
 * @property {string} company - XPath for company information
 * @property {Object} connect - Selectors for connection buttons and dialogs
 * @property {Object} more - Selectors for "More" menu options
 */
const XPATHS = {
    name: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1",
    name2: "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1",
    company: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button/span/div",
    company2: "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li/button/span/div",
    connect: {
        btn: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button",
        btn2: "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button",
        addNote: "/html/body/div[3]/div/div/div[3]/button[1]",
        textArea: "/html/body/div[3]/div/div/div[2]/div/textarea",
        send: "/html/body/div[3]/div/div/div[3]/button[2]"
    },
    more: {
        btn: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button",
        btn2: "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button",
        connect: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div",
        addNote: "/html/body/div[3]/div/div/div[3]/button[1]",
        textArea: "/html/body/div[3]/div/div/div[2]/div/textarea",
        send: "/html/body/div[3]/div/div/div[3]/button[2]",
        pending: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div/span"
    },
    nextPerson: "/html/body/div[5]/div[3]/div/div/div[2]/div/div/aside/section[2]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div[1]/div/div/div/span[1]",
    pendingRequest: "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
};

/**
 * CSS selectors for LinkedIn company page elements.
 *
 * @constant {Object} SELECTORS
 */
const SELECTORS = {
    profileCard: '.org-people-profile-card',
    connectButton: 'button[aria-label^="Invite"]',
    nameElement: '.org-people-profile-card__profile-info .lt-line-clamp--single-line',
    addNoteButton: '.artdeco-button[aria-label="Add a note"]',
    messageTextArea: 'textarea[name="message"]',
    sendButton: '.artdeco-button[aria-label="Send now"]',
    dismissButton: 'button[aria-label="Dismiss"]',
    emailLabel: 'label[for="email"]',
    invitationCard: 'li.invitation-card',
    withdrawButton: 'span.artdeco-button__text',
    confirmButton: 'button[class*="primary"] > span.artdeco-button__text'
};

/**
 * Timing constants for delays and timeouts (in milliseconds).
 *
 * @constant {Object} TIMING
 */
const TIMING = {
    MIN_DELAY: 30000,      // 30 seconds - minimum delay between actions
    MAX_DELAY: 45000,      // 45 seconds - maximum delay between actions
    DEFAULT_TIMEOUT: 10000, // 10 seconds - default element wait timeout
    SHORT_TIMEOUT: 2000,    // 2 seconds - short timeout for optional elements
    POLL_INTERVAL: 100,     // 100ms - interval for checking element visibility
    LONG_POLL_INTERVAL: 500 // 500ms - interval for checking element presence
};

/**
 * LinkedIn automation rate limits and safety constants.
 *
 * @constant {Object} LIMITS
 */
const LIMITS = {
    DEFAULT_CONNECTION_LIMIT: 20,  // Default maximum connections per session
    RECOMMENDED_DAILY_LIMIT: 50,   // Recommended max connections per day
    WARNING_THRESHOLD: 30          // Warn when approaching limits
};

// Export configuration for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        XPATHS,
        SELECTORS,
        TIMING,
        LIMITS
    };
}
