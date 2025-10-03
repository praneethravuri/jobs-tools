function askForCompanyName() {
    const companyName = prompt("Please enter the name of the company:");
    const jobId = prompt("Please enter the job id of the position: ");
    if (companyName) {
        if (jobId) {
            clickConnectAndSendNote(companyName, 20, {jobId: jobId})
        }
        else {
            clickConnectAndSendNote(companyName, 20)
        }
    }
    else {
        console.log("No company name provided.");
    }

}

// Function to simulate a middle-click
function simulateMiddleClick(element) {
    let event = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
        button: 1  // Middle button
    });
    element.dispatchEvent(event);
}


async function clickConnectAndSendNote(companyName, limit, options = {}) {
    const profileCards = document.querySelectorAll('.org-people-profile-card');
    let processedCount = 0;
    const randomDelay = Math.floor(Math.random() * (45000 - 30000 + 1)) + 30000;

    for (const card of profileCards) {
        if (processedCount >= limit) {
            break;
        }

        const connectButton = card.querySelector('button[aria-label^="Invite"]');
        const nameElement = card.querySelector('.org-people-profile-card__profile-info .lt-line-clamp--single-line');

        // if (!connectButton || !nameElement || connectButton.textContent.trim() !== "Connect" || nameElement.textContent.trim() === "LinkedIn Member") {
        //     // await new Promise(resolve => setTimeout(resolve, 10000));

        //     continue;
        // }

        if (!connectButton || connectButton.textContent.trim() === "Message") {
            console.log(`You have to open ${nameElement.textContent.trim()}'s profile in a new tab`)
            continue;
        }
        else if (!nameElement) {
            console.log("Couldn't find the name of the person. Moving on to the next person.");
            continue;
        }
        else if (nameElement.textContent.trim() === "LinkedIn Member") {
            console.log("Encountered LinkedIn Member. Moving on to next person");
            continue;
        }
        else if (connectButton.textContent.trim() === "Pending") {
            console.log(`You have already sent a request to ${nameElement.textContent.trim()}`);
            continue;
        }

        const firstName = nameElement.textContent.trim().split(" ")[0] || "there";
        let message = ''

        if ("jobId" in options) {
            message = `Hi ${firstName}! I'm looking to apply for an SDE role (Job ID: ${options.jobId}) at ${companyName}. Would you be willing to look at my resume or reach out to me if need any additional information? Thanks!`;
        }
        else {
            message = `Hi ${firstName}! I'm looking to apply for an SDE role at ${companyName}. Would you be willing to look at my resume or reach out to me if need any additional information? Thanks!`;
        }

        console.log(`Referral Message for ${firstName}: ${message}`);

        connectButton.click();

        try {
            // Wait for the email label to appear, if it does, close it and move to next
            const emailLabel = await waitForElementVisible('label[for="email"]', 2000).catch(() => null);
            if (emailLabel) {
                document.querySelector('button[aria-label="Dismiss"]').click();
                await new Promise(resolve => setTimeout(resolve, randomDelay));
                continue;
            }

            // Wait for the "Add a Note" button and click it
            await waitForElement('.artdeco-button[aria-label="Add a note"]');
            document.querySelector('.artdeco-button[aria-label="Add a note"]').click();

            // Wait for the text area to be available to enter the message
            await waitForElement('textarea[name="message"]');
            const textArea = document.querySelector('textarea[name="message"]');
            textArea.value = message;
            triggerInputEvent(textArea);

            // Wait for the "Send now" button to be enabled and click it
            await waitForElementEnabled('.artdeco-button[aria-label="Send now"]');
            document.querySelector('.artdeco-button[aria-label="Send now"]').click();
        } catch (error) {
            console.error('An error occurred:', error);
            continue;
        }

        processedCount++;
        console.log(`Referrals sent: ${processedCount}`);
        await new Promise(resolve => setTimeout(resolve, randomDelay));
    }
}

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
            reject(new Error(`Element "${selector}" not visible within ${timeout} ms`));
        }, timeout);
    });
}



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
            reject(new Error(`Element "${selector}" not found within ${timeout} ms`));
        }, timeout);
    });
}

// Function to trigger an input event
function triggerInputEvent(element) {
    const event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });
    element.dispatchEvent(event);
}

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
            reject(new Error(`Element "${selector}" not enabled within ${timeout} ms`));
        }, timeout);
    });
}


askForCompanyName();