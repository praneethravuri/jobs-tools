
function main() {
    let xpaths = {
        "name": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1",
        "name2": "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1",
        "company": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button/span/div",
        "company2": "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li/button/span/div",
        "connect": {
            "btn": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button",
            "btn2": "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button",
            "addNote": "/html/body/div[3]/div/div/div[3]/button[1]",
            "textArea": "/html/body/div[3]/div/div/div[2]/div/textarea",
            "send": "/html/body/div[3]/div/div/div[3]/button[2]"
        },
        "more": {
            "btn": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button",
            "btn2": "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button",
            "connect": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div",
            "addNote": "/html/body/div[3]/div/div/div[3]/button[1]",
            "textArea": "/html/body/div[3]/div/div/div[2]/div/textarea",
            "send": "/html/body/div[3]/div/div/div[3]/button[2]",
            "pending": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div/span"
        },
        "nextPerson": "/html/body/div[5]/div[3]/div/div/div[2]/div/div/aside/section[2]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div[1]/div/div/div/span[1]",
        "pendingRequest": "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
    }

    // For getting the name and the company where the person is working
    function getTextByXpath(xpath) {
        let result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        return result.singleNodeValue ? result.singleNodeValue.textContent.trim() : '';
    }

    let nameText = getTextByXpath(xpaths["name"]);
    if (!nameText) {
        nameText = getTextByXpath(xpaths["name2"]);
    }
    let companyText = getTextByXpath(xpaths["company"]);
    if (!companyText) {
        companyText = getTextByXpath(xpaths["company2"]);
    }

    // to know if the button is present or not
    function isElementPresentByXpath(xpath, options = {}) {
        let result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        let element = result.singleNodeValue;
        if (!element) {
            return false;
        }
        if ('textToMatch' in options && element.textContent.trim() !== options.textToMatch) {
            return false;
        }
        return true;
    }

    let connectBtnPresent = isElementPresentByXpath(xpaths["connect"]["btn"], { textToMatch: "Connect" });
    let connectBtnPresent2 = isElementPresentByXpath(xpaths["connect"]["btn2"], { textToMatch: "Connect" });
    console.log("connectBtnPresent", connectBtnPresent);
    console.log("connectBtnPresent2", connectBtnPresent2);
    let moreBtnPresent = isElementPresentByXpath(xpaths["more"]["btn"], { textToMatch: "More" });
    let moreBtnPresent2 = isElementPresentByXpath(xpaths["more"]["btn2"], { textToMatch: "More" });
    console.log("moreBtnPresent", moreBtnPresent);
    console.log("moreBtnPresent2", moreBtnPresent2);
    let nextPersonBtnPresent = isElementPresentByXpath(xpaths["nextPerson"]);
    console.log("nextPersonBtnPresent", nextPersonBtnPresent);
    let pendingRequestBtnPresent = isElementPresentByXpath(xpaths["pendingRequest"], { textToMatch: "Pending" });
    console.log("pendingRequestBtnPresent", pendingRequestBtnPresent)
    let morePendingBtnPresent = isElementPresentByXpath(xpaths["more"]["pending"], { textToMatch: "Pending" });
    console.log("morePendingBtnPresent", morePendingBtnPresent)

    function clickElementWhenVisible(xpath, maxWaitTime = 5000) {
        let intervalTime = 100; // Interval time in milliseconds
        let elapsedTime = 0;

        let intervalId = setInterval(() => {
            let result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            let element = result.singleNodeValue;

            // Check if element is found and visible
            if (element && element.offsetParent !== null) {
                clearInterval(intervalId);
                element.click();
                console.log("Element clicked");
            } else {
                elapsedTime += intervalTime;
                if (elapsedTime >= maxWaitTime) {
                    clearInterval(intervalId);
                    console.log("Timeout: Element not found or visible for the given XPath within the maximum wait time");
                }
            }
        }, intervalTime);
    }

    function setTextWhenVisible(xpath, text, maxWaitTime = 5000) {
        let intervalTime = 100; // Interval time in milliseconds
        let elapsedTime = 0;

        let intervalId = setInterval(() => {
            let result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            let textArea = result.singleNodeValue;

            // Check if text area is found and visible
            if (textArea && textArea.offsetParent !== null) {
                clearInterval(intervalId);
                textArea.value = text;
                console.log("Text set in text area");

                // Dispatch an input event
                let event = new Event('input', { bubbles: true });
                textArea.dispatchEvent(event);
                console.log("Input event dispatched");

            } else {
                elapsedTime += intervalTime;
                if (elapsedTime >= maxWaitTime) {
                    clearInterval(intervalId);
                    console.log("Timeout: Text area not found or visible for the given XPath within the maximum wait time");
                }
            }
        }, intervalTime);

        clickElementWhenVisible(xpaths["connect"]["send"])
    }

    function moveToNextPerson() {
        // Move to the next person after sending the referral
        if (nextPersonBtnPresent) {
            // clickElementWhenVisible(xpaths["nextPerson"]);
            console.log("Done with this person");
        }
        else {
            console.error("The next person is not visible");
        }
        return;
    }

    let recruiterGeneratedText = `Hi ${nameText.split(" ")[0]}! I noticed that you are a recruiter at {COMPANY_NAME}. I'm a CS grad from GMU looking for new opportunities and wonder if I might fit any roles you have. Could we discuss this further? Thanks!`

    let referralGeneratedText = `Hi ${nameText.split(" ")[0]}! I noticed that you are working at {COMPANY_NAME}. I'm a CS grad from GMU looking for new opportunities and wonder if you could refer me to the {POSITION_NAME} position. Thanks!`

    // console.log(generatedText);

    let generatedText = referralGeneratedText;
    console.log(generatedText);

    // If the connect button is present
    // You will click on the connect button
    // Click on the add note button
    // Insert the generated text in the text area
    // Click on the send button
    let connectBtnXPath = '';
    if (connectBtnPresent) {
        console.log("Connect button is present");
        connectBtnXPath = xpaths["connect"]["btn"];
    } else if (connectBtnPresent2) {
        console.log("Connect button is present");
        connectBtnXPath = xpaths["connect"]["btn2"];
    }

    if (connectBtnXPath) {
        clickElementWhenVisible(connectBtnXPath);
        clickElementWhenVisible(xpaths["connect"]["addNote"]);
        setTextWhenVisible(xpaths["connect"]["textArea"], generatedText);
        clickElementWhenVisible(xpaths["connect"]["send"]);
        moveToNextPerson();
    }

    // If the connect button is not present and the more button is present
    // You will click on the more button
    // You will click on the connect button
    // Click on the add note button
    // Insert the generated text in the text area
    // Click on the send button
    let moreBtnXpath = '';
    if (moreBtnPresent) {
        moreBtnXpath = xpaths["more"]["btn"];
    } else if (moreBtnPresent2) {
        moreBtnXpath = xpaths["more"]["btn2"];
    }

    if (moreBtnXpath) {
        if (morePendingBtnPresent) {
            console.log("You have already sent a request to this person");
            moveToNextPerson();
        } else {
            console.log("More button is required to be clicked");
            clickElementWhenVisible(moreBtnXpath); // Use the variable here
            clickElementWhenVisible(xpaths["more"]["connect"]);
            clickElementWhenVisible(xpaths["more"]["addNote"]);
            setTextWhenVisible(xpaths["more"]["textArea"], generatedText);
            clickElementWhenVisible(xpaths["more"]["send"]);
            moveToNextPerson();
        }
    }


    // If the pending button is present, it means that you have already sent a referral request. You will then be moved to the next person
    else if (pendingRequestBtnPresent) {
        console.log("Pending request button is present");
        moveToNextPerson();
    }

    else {
        console.log("here");
    }
}

main();     