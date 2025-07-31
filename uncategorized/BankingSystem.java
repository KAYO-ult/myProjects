import java.util.*;

class User {
    private String name;
    private String email;
    private String password;
    private double balance;

    public User(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.balance = 0;
    }

    public String getEmail() {
        return email;
    }

    public boolean authenticate(String password) {
        return this.password.equals(password);
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposited Successfully!");
    }

    public void withdraw(double amount) {
        if (balance >= amount) {
            balance -= amount;
            System.out.println("Withdrawn Successfully!");
        } else {
            System.out.println("Insufficient Balance!");
        }
    }
}

public class BankingSystem {
    private static Scanner sc = new Scanner(System.in);
    private static User currentUser;

    public static void main(String[] args) {
        menu();
    }

    public static void menu() {
        while (true) {
            System.out.println("1. Register\n2. Login\n3. Exit");
            int choice = sc.nextInt();
            sc.nextLine();
            switch (choice) {
                case 1: register(); break;
                case 2: login(); break;
                case 3: System.exit(0);
                default: System.out.println("Invalid choice!");
            }
        }
    }

    public static void register() {
        System.out.print("Enter Name: ");
        String name = sc.nextLine();
        System.out.print("Enter Email: ");
        String email = sc.nextLine();
        System.out.print("Enter Password: ");
        String password = sc.nextLine();

        currentUser = new User(name, email, password);
        System.out.println("Registered Successfully!");
    }

    public static void login() {
        if (currentUser == null) {
            System.out.println("No registered users. Please register first.");
            return;
        }
        
        System.out.print("Enter Email: ");
        String email = sc.nextLine();
        System.out.print("Enter Password: ");
        String password = sc.nextLine();

        if (currentUser.getEmail().equals(email) && currentUser.authenticate(password)) {
            System.out.println("Welcome, " + email);
            accountMenu();
        } else {
            System.out.println("Invalid Credentials!");
        }
    }

    public static void accountMenu() {
        while (true) {
            System.out.println("1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout");
            int choice = sc.nextInt();
            switch (choice) {
                case 1: System.out.println("Your Balance: " + currentUser.getBalance()); break;
                case 2: deposit(); break;
                case 3: withdraw(); break;
                case 4: return;
                default: System.out.println("Invalid choice!");
            }
        }
    }

    public static void deposit() {
        System.out.print("Enter amount to deposit: ");
        double amount = sc.nextDouble();
        currentUser.deposit(amount);
    }

    public static void withdraw() {
        System.out.print("Enter amount to withdraw: ");
        double amount = sc.nextDouble();
        currentUser.withdraw(amount);
    }
}