import tkinter as tk
from tkinter import filedialog
import re
import ipaddress

# Определяем функцию
def my_function():
    # Открываем диалоговое окно для выбора нескольких файлов
    file_paths = filedialog.askopenfilenames()

    # Создаем множество для хранения уникальных IP-адресов
    ip_addresses = set()

    # Открываем каждый выбранный файл и выполняем действие для каждой строки в файле
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Извлекаем IP-адрес или диапазон IP-адресов из строки
                    ip_range = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}-\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                    if ip_range:
                        # Если диапазон IP-адресов найден, обрабатываем его
                        start_ip, end_ip = ip_range.group().split('-')
                        start_ip = ipaddress.ip_address(start_ip)
                        end_ip = ipaddress.ip_address(end_ip)
                        for ip in range(int(start_ip), int(end_ip) + 1):
                            # Добавляем каждый IP-адрес в множество
                            ip_addresses.add(str(ipaddress.ip_address(ip)))
                    else:
                        ip_address = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?\b', line)
                        if ip_address:
                            # Если IP-адрес найден, обрабатываем его
                            ip_network = ipaddress.ip_network(ip_address.group(), strict=False)
                            for ip in ip_network.hosts():
                                # Добавляем каждый IP-адрес в множество
                                ip_addresses.add(str(ip))

        except Exception as e:
            # Если возникла ошибка, выводим сообщение об ошибке
            pass

    # Сортируем список уникальных IP-адресов
    ip_addresses = sorted(ip_addresses)

    # Добавляем каждый уникальный IP-адрес в текстовое поле
    for ip in ip_addresses:
        if ipaddress.ip_address(ip).is_private:
            text_field2.insert(tk.END, ip + '\n')
        else:
            text_field.insert(tk.END, ip + '\n')


# Определяем функцию для сохранения текста из текстового поля
def save_text():
    # Открываем диалоговое окно для выбора файла для сохранения
    file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Сохраняем текст из текстового поля в файл
    try:
        with open(file_path, 'w') as file:
            file.write(text_field.get("1.0", tk.END))
    except Exception as e:
        # Если возникла ошибка, выводим сообщение об ошибке
        print("Ошибка при сохранении файла:", e)

# Определяем функцию для сохранения текста из второго текстового поля
def save_local_text():
    # Открываем диалоговое окно для выбора файла для сохранения
    file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Сохраняем текст из второго текстового поля в файл
    try:
        with open(file_path, 'w') as file:
            file.write(text_field2.get("1.0", tk.END))
    except Exception as e:
        # Если возникла ошибка, выводим сообщение об ошибке
        print("Ошибка при сохранении файла:", e)

# Создаем окно
root = tk.Tk()
root.title("IP Address Extractor")
root.geometry("600x400")

# Создаем первую кнопку и привязываем к ней функцию
button1 = tk.Button(root, text="Load ips", command=my_function, bg="lightblue", fg="black", font=("Helvetica", 12))
button1.pack(side=tk.LEFT, padx=10, pady=10)

# Создаем вторую кнопку и привязываем к ней функцию
button2 = tk.Button(root, text="Save global", command=save_text, bg="lightblue", fg="black", font=("Helvetica", 12))
button2.pack(side=tk.TOP, padx=10, pady=10)

# Создаем третью кнопку и привязываем к ней функцию
button3 = tk.Button(root, text="Save local", command=save_local_text, bg="lightblue", fg="black", font=("Helvetica", 12))
button3.pack(side=tk.BOTTOM, padx=10, pady=10)

# Создаем текстовое поле
text_field = tk.Text(root, height=10, width=50, bg="white", fg="black", font=("Helvetica", 12))
text_field.pack(side=tk.TOP, padx=10, pady=10)

# Создаем второе текстовое поле
text_field2 = tk.Text(root, height=10, width=50, bg="white", fg="black", font=("Helvetica", 12))
text_field2.pack(side=tk.BOTTOM, padx=10, pady=10)

# Запускаем главный цикл
root.mainloop()
