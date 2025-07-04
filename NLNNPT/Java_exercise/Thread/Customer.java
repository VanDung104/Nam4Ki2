class Customer implements Runnable {
    private CoffeeShop shop;

    public Customer(CoffeeShop shop) {
        this.shop = shop;
    }

    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            shop.takeCoffee();
            try {
                Thread.sleep(2000); // Mô phỏng thời gian uống cà phê
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
