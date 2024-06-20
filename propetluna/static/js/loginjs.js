document.getElementById("login-form").addEventListener("submit", function(event){
    event.preventDefault(); // Prevent the form from submitting

    // Get the username and password values
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // You can perform validation here before sending the data to the server
    // For simplicity, I'm just logging the values
    console.log("Username: " + username);
    console.log("Password: " + password);

    // Here you can send the username and password to the server using AJAX or any other method
});
