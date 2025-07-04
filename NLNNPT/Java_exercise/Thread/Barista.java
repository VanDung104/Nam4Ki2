class Barista implements Runnable {
    private CoffeeShop shop;

    public Barista(CoffeeShop shop) {
        this.shop = shop;
    }

    @Override
    public void run() {
        String[] menu = {"Espresso", "Latte", "Cappuccino", "Mocha", "Americano"};
        for (String coffee : menu) {
            shop.makeCoffee(coffee);
            try {
                Thread.sleep(1000); // Mô phỏng thời gian pha chế
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
