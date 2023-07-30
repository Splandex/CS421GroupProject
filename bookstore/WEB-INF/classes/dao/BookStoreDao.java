package dao;

import java.sql.*;
import java.util.ArrayList;
import beans.*;

public class BookStoreDao {
    Connection con;

    public BookStoreDao() throws ClassNotFoundException, SQLException {
        Class.forName("com.mysql.jdbc.Driver");
        String url = "jdbc:mysql://127.0.0.1:3306/project";
        con = DriverManager.getConnection(url, "root", "Password3306");
    }

    public User userlogin(User userp) throws SQLException {

        String sql = "SELECT * FROM user WHERE userName = ? AND password = ?";
        PreparedStatement pStmt = con.prepareStatement(sql);

        pStmt.setString(1, userp.getUserName());
        pStmt.setString(2, userp.getPassword());
        User user = null;
        ResultSet rs = pStmt.executeQuery();

        if (rs.next()) {
            user = new User();
            user.setEmail(rs.getString("email"));
            user.setAddress(rs.getString("address"));
            user.setPhone(rs.getString("phone"));
            user.setUserName(rs.getString("userName"));
            user.setPassword(rs.getString("password"));
            user.setStatus(rs.getString("status"));
            return user;
        } else {
            return null;
        }

    }
    
    public Boolean signup(User user) throws SQLException {

        String sql = "INSERT INTO user (userName,email,password,address,phone, status) VALUES(?,?,?,?,?,?)";
        PreparedStatement pStmt = con.prepareStatement(sql);

        pStmt.setString(1, user.getUserName());
        pStmt.setString(2, user.getEmail());
        pStmt.setString(3, user.getPassword());
        pStmt.setString(4, user.getAddress());
        pStmt.setString(5, user.getPhone());
        pStmt.setString(6, user.getStatus());
        int rs = pStmt.executeUpdate();

        if (rs > 0) {
            return true;

        } else {
            return false;
        }
    }

}