<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup</title>
    <script src="./signup.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="form">
    <form name="signup" action="signup" method="post" onsubmit="return validate()">
        <h1>SIGN UP</h1>
        <input type="text" name="name" placeholder="User Name" onchange="name_validate()">
        <input type="text" name="email" placeholder="Email" onchange="email_validate()">
        <input type="password" name="password" placeholder="Password" onblur="pass_validate()">
        <input type="password" name="confirm_password" placeholder="Confirm Password" onchange="confirm_pass()">
        <input type="text" name="address" placeholder="Address" onchange="address_validate()">
        <input type="text" name="phone" placeholder="Phone" onchange="phone_validate()">
        <button type="submit" id="submit">Sign Up</button>
        <p class="message">Have Account? <a href="login.jsp">Log In</a>
    </form> 
    </div>
</body>
</html>