import java.io.*;
import beans.*;
import dao.*;

import javax.servlet.http.*;

public class Logout extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        HttpSession session = request.getSession(false);
        if(session != null) session.invalidate();
        response.sendRedirect("login.jsp");
        ;

    }

}
