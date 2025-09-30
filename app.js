// Initialize Telegram WebApp
let tg = window.Telegram.WebApp;

// Expand the WebApp to full height
tg.expand();

// Configure the MainButton appearance
tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

// Variable to store the user IP
let userip = "";

// Fetch the user IP from ipify API
fetch('https://api.ipify.org/?format=json')
  .then(response => response.json())
  .then(data => {
    userip = data.ip;
    console.log('User IP Address:', userip);

    // Set button text and show it after IP is fetched
    tg.MainButton.setText("Click to complete the verification");
    tg.MainButton.show();
  })
  .catch(error => {
    console.error('Error retrieving IP address:', error);
    // Optional: show error message in the WebApp
    let errorMsg = document.createElement("p");
    errorMsg.innerText = "⚠️ Could not fetch IP. Please try again.";
    document.getElementById("usercard").appendChild(errorMsg);
  });

// When MainButton is clicked, send the IP to the bot
Telegram.WebApp.onEvent("mainButtonClicked", function() {
  if (userip !== "") {
    tg.sendData(userip); // Send IP back to Bots.Business bot
  } else {
    alert("IP not ready yet. Please wait a moment.");
  }
});

// Display user's first and last name inside the WebApp
let usercard = document.getElementById("usercard");
let p = document.createElement("p");
p.innerText = `${tg.initDataUnsafe.user.first_name} ${tg.initDataUnsafe.user.last_name}`;
usercard.appendChild(p);
