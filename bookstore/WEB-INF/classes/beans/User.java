package beans;

public class User {
    public String userName;
    public String email;
    public String password;
    public String address;
    public String phone;
    public String status;

    public User() {
        this.email = "";
        this.userName = "";
        this.password = "";
        this.address = "";
        this.phone = "";
        this.status = "active";
    }

    public User(String email, String userName, String password, String address, String phone, String status) {
        this.email = email;
        this.userName = userName;
        this.password = password;
        this.address = address;
        this.phone = phone;
        this.status = status;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getStatus(){
        return status;
    }

    public void setStatus(String status){
        this.status = status;
    }

    @Override
    public String toString() {
        return " Name: " + this.userName + "\n  Email: " + this.email + "Password: " + this.password
                + "Address: " + this.address + "Phone: " + this.phone;
    }
}
