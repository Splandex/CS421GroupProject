<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <script src="./login.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <%
        String msg = request.getParameter("msg");
    %>
    <form action="login" method="post"">   
        <div class="form">
            <h1>Login</h1>
            <input type="text" name="userName" placeholder="Enter Username">
            <input type="password" name="password" placeholder="Enter Password" >
            <div style="color:red">${msg}</div>
            <button type="submit" id="submit">Login</button>
            <p class="message">Not Have Account? <a href="signup.jsp">Sign Up</a></p>
        </div>
    </form>
</body>
</html>