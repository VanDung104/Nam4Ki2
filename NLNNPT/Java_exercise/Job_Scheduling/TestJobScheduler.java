import java.util.Date;

public class TestJobScheduler {
    public static void main(String[] args) {
        JobScheduler scheduler = new JobScheduler(3);

        // Báo cáo 1: Gửi ngay lập tức
        Runnable reportJob1 = new Runnable() {
            @Override
            public void run() {
                System.out.println("Gửi báo cáo 1: " + new Date());
                System.out.println("Cập nhật dữ liệu cho báo cáo 1: " + new Date());
            }
        };
        scheduler.execute(reportJob1);

        // Báo cáo 2: Gửi sau 5 giây
        Runnable reportJob2 = new Runnable() {
            @Override
            public void run() {
                System.out.println("Gửi báo cáo 2: " + new Date());
                System.out.println("Cập nhật dữ liệu cho báo cáo 2: " + new Date());
            }
        };
        scheduler.executeIn(reportJob2, 5000);

        //Kiểm tra hệ thống sau 5 giây
        Runnable healthCheckJob = new Runnable() {
            @Override
            public void run() {
                System.out.println("Kiểm tra hệ thống: " + new Date());
            }
        };
        scheduler.executeIn(healthCheckJob, 5000);

        //Sao lưu dữ liệu mỗi 10 giây, lặp lại 3 lần
        Runnable backupJob = new Runnable() {
            @Override
            public void run() {
                System.out.println("Đang sao lưu dữ liệu: " + new Date());
            }
        };
        scheduler.executeInAndRepeat(backupJob, 10000, 10000, 3);

        // Chờ chương trình chạy 40 giây để kiểm tra kết quả
        try {
            Thread.sleep(40000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
