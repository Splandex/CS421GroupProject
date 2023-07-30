import java.io.*;
import java.sql.SQLException;
import dao.*;

import javax.servlet.ServletException;
import javax.servlet.http.*;
import beans.*;

public class LoginServlet extends HttpServlet {
    BookStoreDao dao;

    public void init() {
        try {
            dao = new BookStoreDao();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {

        String name = request.getParameter("userName");
        String password = request.getParameter("password");

        try {
            User user = new User();
            user.setUserName(name);
            user.setPassword(password);

            User verifed_user = null;// = new User();

            verifed_user = dao.userlogin(user);

            if (verifed_user != null) {
                if((verifed_user.getStatus()).equals("blocked")){
                    request.setAttribute("msg", "You are Blocked. Contact your admin.");
                    request.getRequestDispatcher("login.jsp").forward(request, response);
                } else {
                    HttpSession session = request.getSession();
                    session.setAttribute("username", name);
                    session.setAttribute("status",verifed_user.getStatus());
                    response.sendRedirect("userHome.jsp");
                }

            } else {
                request.setAttribute("msg", "Invalid email or password");
                request.getRequestDispatcher("login.jsp").forward(request, response);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

    }
}