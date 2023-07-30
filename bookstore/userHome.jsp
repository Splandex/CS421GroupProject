<%
if(session.getAttribute("username") == null){
    response.sendRedirect("login.jsp");
}

String username = (String) session.getAttribute("username");
%>
<%@ page isErrorPage="false" errorPage="error.jsp" %>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>User Home</title>
        <link rel="stylesheet" href="stylehome.css" />
        <style>
            .logout_button{
                font-family: "Roboto", sans-serif;
                text-transform: uppercase;
                outline: 0;
                background: #165800;
                margin:  10px;
                padding: 15px;
                color:#ffffff;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <h1><center>HOME Status: <%=session.getAttribute("status")%></center></h1>
        <div class="form">
            <a href="searchBook.jsp">
                <button id="submit">Search Book</button>
            </a>
            <a href='cartList.jsp?username=<%=username%>'>
                <button id="submit">View Cart</button>
            </a>
            <br>
            <div style="color:red">${msg}</div>
        </div>
        <a href="logout"><button class="logout_button">LOG OUT</button></a>
    </body>
</html>
