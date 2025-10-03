/**
 * LinkedIn Connection Request Withdrawal Automation
 *
 * Automatically withdraws pending LinkedIn connection requests to clean up
 * your network and maintain a professional profile. Useful for removing old,
 * unaccepted connection requests.
 *
 * @fileoverview Bulk withdraw pending LinkedIn connection requests
 * @author Your Name (Adapted from https://medium.com/@matijazib)
 * @version 2.0.0
 *
 * @usage
 * 1. Navigate to LinkedIn → My Network → Manage → Sent
 * 2. Open browser DevTools console
 * 3. Paste and run this script
 * 4. Script will automatically withdraw all pending requests
 *
 * @warning
 * - Use responsibly - this action cannot be undone easily
 * - LinkedIn's terms of service prohibit automation
 * - Consider withdrawing only very old requests (6+ months)
 */

/**
 * Withdraw all pending LinkedIn connection invitations.
 *
 * This function finds all pending invitation cards on the current page,
 * clicks the withdraw button for each, confirms the withdrawal, and adds
 * a random delay between actions to appear more human-like.
 *
 * @async
 * @returns {Promise<void>} Promise that resolves when all withdrawals complete
 *
 * @example
 * // Run from LinkedIn's "Sent invitations" page
 * await withdrawInvitations();
 */
async function withdrawInvitations() {
    const invitations = Array.from(
        document.querySelectorAll("li.invitation-card")
    );

    if (invitations.length === 0) {
        console.log("⚠️  No pending invitations found on this page.");
        console.log("   Make sure you're on the 'Sent' invitations page.");
        return;
    }

    console.log(`🔍 Found ${invitations.length} pending invitations`);
    console.log("🚀 Starting withdrawal process...\n");

    let count = 0;

    for (let invitation of invitations) {
        const withdrawButton = invitation.querySelector(
            "span.artdeco-button__text"
        );

        if (withdrawButton) {
            // Click the withdraw button
            withdrawButton.click();

            // Wait for confirmation dialog and click confirm
            const confirmButton = await new Promise((resolve) => {
                const interval = setInterval(() => {
                    const button = document.querySelector(
                        'button[class*="primary"] > span.artdeco-button__text'
                    );
                    if (button) {
                        clearInterval(interval);
                        resolve(button);
                    }
                }, 100); // Check every 100ms
            });

            confirmButton.click();

            // Exit if we've processed all invitations
            if (count >= invitations.length) {
                return;
            }

            count++;
            console.log(`✅ Withdrawn ${count}/${invitations.length} invitations`);

            // Random delay between 500ms and 3000ms to appear human
            const delay = Math.random() * 2500 + 500;
            await new Promise((resolve) => setTimeout(resolve, delay));
        }
    }

    console.log(`\n🎉 Process complete! Withdrawn ${count} connection requests.`);
    console.log("   Refresh the page to see remaining invitations (if any).");
}

// Start the withdrawal process
withdrawInvitations();