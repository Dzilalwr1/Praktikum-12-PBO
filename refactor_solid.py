from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Konfiguraasi dasar: Smuea log level INFO ke atas akan di tampilkan
# Format: Waktu - Level - Nama Kelas/Fungsi - Pesan
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s %(message)s'
)
# Tambahkan logger untuk kelas yang akan kita gunakan
LOGGER = logging.getLogger('CheckoutSystem')

@dataclass
class Order:
    """Model data sederhana untuk pesanan. [cite: 33]"""
    customer_name: str
    total_price: float
    status: str = "open"

# --- ABSTRAKSI ---
class IPaymentProcessor(ABC):
    """Interface untuk prosesor pembayaran. [cite: 34]"""
    @abstractmethod
    def process(self, order: Order) -> bool:
        """Metode abstrak untuk memproses pembayaran."""
        pass

class INotificationService(ABC):
    """Interface untuk layanan notifikasi. [cite: 34]"""
    @abstractmethod
    def send(self, order: Order):
        """Metode abstrak untuk mengirim notifikasi."""
        pass

# --- IMPLEMENTASI KONKRIT ---
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        # Ganti print() dengan logging [cite: 52]
        LOGGER.info(f"Memproses pembayaran Kartu Kredit untuk {order.customer_name}.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        # Ganti print() dengan logging [cite: 52]
        LOGGER.info(f"Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR ---
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran. [cite: 36]
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP). [cite: 37]
    """

    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Menginisialisasi CheckoutService dengan dependensi yang diperlukan. [cite: 40]

        Args:
            payment_processor (IPaymentProcessor): Implementasi interface pembayaran. [cite: 42]
            notifier (INotificationService): Implementasi interface notifikasi. [cite: 42]
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        # Logging alih-alih print() [cite: 56, 57]
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}")
        
        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            LOGGER.info("Checkout Sukses. Status pesanan: PAID.")
            return True
        else:
            # Gunakan level ERROR/WARNING untuk masalah
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.")
            return False

# === PROGRAM UTAMA ===
if __name__ == "__main__":
    andi_order = Order("Andi", 500000)
    email_service = EmailNotifier()
    cc_processor = CreditCardProcessor()

    checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
    checkout_cc.run_checkout(andi_order)