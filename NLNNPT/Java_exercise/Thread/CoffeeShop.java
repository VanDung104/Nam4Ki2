import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

class CoffeeShop {
    private BlockingQueue<String> coffeeQueue = new LinkedBlockingQueue<>(1); // Chỉ chứa 1 ly cà phê mỗi lần

    public void makeCoffee(String coffee) {
        try {
            coffeeQueue.put(coffee); // Đặt cà phê vào hàng đợi (Chờ nếu đầy)
            System.out.println("Nhân viên pha chế đã pha: " + coffee);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public void takeCoffee() {
        try {
            String coffee = coffeeQueue.take(); // Lấy cà phê (Chờ nếu chưa có)
            System.out.println("Khách hàng nhận được: " + coffee);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
