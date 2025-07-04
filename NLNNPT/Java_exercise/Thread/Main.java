public class Main {
    public static void main(String[] args) {
        CoffeeShop shop = new CoffeeShop();

        Thread baristaThread = new Thread(new Barista(shop));  // Tạo luồng nhân viên pha chế
        Thread customerThread = new Thread(new Customer(shop)); // Tạo luồng khách hàng

        baristaThread.start();
        customerThread.start();
    }
}
