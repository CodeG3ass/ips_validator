import os
import re
import ipaddress
import threading
from openpyxl import Workbook
from typing import List, Set
from tkinter import Tk, filedialog, messagebox

# Decorators
def synchronized(lock):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator

# Helper function to parse IP, range, or CIDR
def parse_ip_ranges(ip_range: str) -> Set[str]:
    """Parse a single IP, range, or CIDR notation to a set of IPs."""
    try:
        # Проверка диапазона IP (например, '192.168.1.1-192.168.1.10')
        if "-" in ip_range:
            start_ip, end_ip = map(ipaddress.ip_address, ip_range.split("-"))
            return {str(ip) for ip in ipaddress.summarize_address_range(start_ip, end_ip)}
        
        # Проверка CIDR (например, '192.168.1.0/24')
        elif "/" in ip_range:
            network = ipaddress.ip_network(ip_range, strict=False)
            return {str(ip) for ip in network.hosts()}  # Получаем все хосты в сети
        
        # Проверка одиночного IP (например, '192.168.1.1')
        else:
            ip = ipaddress.ip_address(ip_range)  # Проверка и преобразование в IP
            return {str(ip)}
    
    except ValueError:
        return set()

# Context Manager
class PathSelector:
    def __enter__(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Select Path", "Please select the folder containing .txt files.")

        folder_path = filedialog.askdirectory(title="Select Folder with .txt Files")

        if folder_path:
            # Ask for the destination folder to save the output files
            save_folder = filedialog.askdirectory(title="Select Folder to Save Output Files")

            if save_folder:
                return folder_path, save_folder, "folder"
            else:
                raise FileNotFoundError("No destination folder was selected.")
        else:
            raise FileNotFoundError("No folder containing .txt files was selected.")

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup or logging if needed
        pass

# Custom Exceptions
class InvalidIPAddressError(Exception):
    pass

# Classes
class IPProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.lock = threading.Lock()  # For synchronizing thread operations

    def validate_ip(self, ip: str):
        try:
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            raise InvalidIPAddressError(f"Invalid IP address: {ip}")

    def is_private(self, ip: str) -> bool:
        return ipaddress.IPv4Address(ip).is_private

    def extract_ips_from_file(self, file_path: str) -> Set[str]:
        with open(file_path, 'r') as file:
            content = file.read()
        ip_patterns = re.findall(r"(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2}|(?:-\d{1,3}\.){3}\d{1,3})?", content)
        ips = set()
        for ip_pattern in ip_patterns:
            ips.update(parse_ip_ranges(ip_pattern))
        return ips

    def save_to_txt(self, data: List[str], file_name: str):
        output_path = os.path.join(self.output_path, file_name)
        with open(output_path, 'w') as file:
            file.write("\n".join(data))

    def save_to_excel(self, data: List[str], file_name: str):
        wb = Workbook()
        sheet = wb.active
        sheet.title = "IPs"

        for row, ip in enumerate(data, start=1):
            sheet.cell(row=row, column=1, value=ip)

        output_path = os.path.join(self.output_path, file_name)
        wb.save(output_path)

    def process(self):
        """Processes the selected path."""
        all_ips = set()
        private_ips = set()

        threads = []
        for file_name in os.listdir(self.input_path):
            file_path = os.path.join(self.input_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.txt'):
                thread = threading.Thread(target=self._process_file, args=(file_path, all_ips, private_ips))
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        sorted_ips = sorted(all_ips, key=lambda ip: ipaddress.IPv4Address(ip))
        sorted_private_ips = sorted(private_ips, key=lambda ip: ipaddress.IPv4Address(ip))

        self.save_to_txt(sorted_ips, 'all_ips.txt')
        self.save_to_txt(sorted_private_ips, 'private_ips.txt')
        self.save_to_excel(sorted_ips, 'all_ips.xlsx')

    def _process_file(self, file_path: str, all_ips: Set[str], private_ips: Set[str]):
        ips = self.extract_ips_from_file(file_path)
        self._process_ips(ips, all_ips, private_ips)

    def _process_ips(self, ips: Set[str], all_ips: Set[str], private_ips: Set[str]):
        for ip in ips:
            try:
                self.validate_ip(ip)
                with self.lock:  # Ensure thread-safe access to shared data
                    all_ips.add(ip)
                    if self.is_private(ip):
                        private_ips.add(ip)
            except InvalidIPAddressError as e:
                print(e)

# Main function
def main():
    with PathSelector() as (input_path, output_path, path_type):
        processor = IPProcessor(input_path, output_path)
        processor.process()

if __name__ == "__main__":
    main()
