// Shamelessly taken from:
// https://medium.com/@matijazib/withdraw-all-your-linkedin-connection-requests-in-a-few-seconds-with-simple-javascript-f69e022670ea

async function withdrawInvitations() {
    const invitations = Array.from(
      document.querySelectorAll("li.invitation-card")
    );

    console.log(invitations.length);
    let count = 0;
  
    for (let invitation of invitations) {
      const withdrawButton = invitation.querySelector(
        "span.artdeco-button__text"
      );
  
      if (withdrawButton) {
        withdrawButton.click();
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
        if(count >= invitations.length){
            return;
        }
        count++;
        console.log(`Count: ${count}`);
        await new Promise((resolve) =>
          setTimeout(resolve, Math.random() * 2500 + 500)
        );
      }
    }
  }
  
  withdrawInvitations();