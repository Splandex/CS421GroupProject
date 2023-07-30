import java.io.*;
import java.sql.SQLException;
import javax.servlet.http.*;
import beans.*;
import dao.*;

public class SignupServlet extends HttpServlet {

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {

        try {
            handleSignup(request, response);
        } catch (SQLException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

    }

    public void handleSignup(HttpServletRequest request, HttpServletResponse response)
            throws SQLException, ClassNotFoundException, IOException {

        String name = request.getParameter("name");
        String password = request.getParameter("password");
        String email = request.getParameter("email");
        String address = request.getParameter("address");
        String phone = request.getParameter("phone");

        BookStoreDao dao = new BookStoreDao();

        User user = new User();

        user.setUserName(name);
        user.setPassword(password);
        user.setEmail(email);
        user.setAddress(address);
        user.setPhone(phone);
        Boolean flag = false;
        try {
            flag = dao.signup(user);
            if (flag) {
                response.sendRedirect("login.jsp");
            } else {
                response.sendRedirect("signup.jsp");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
