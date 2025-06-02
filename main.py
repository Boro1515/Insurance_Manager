#main.py
import customtkinter
import requests

API_URL = "http://127.0.0.1:8001"

def delete_insured(insured_id):
    try:
        print(f"🗑️ DELETE ID: {insured_id}")
        response = requests.delete(f"{API_URL}/insured/{insured_id}")
        response.raise_for_status()
        print(f"✅ Smazán pojištěenec s ID {insured_id}")
        show_insured()
    except requests.exceptions.RequestException as e:
        print("❌ DELETE chyba:", e)

def edit_insured(person):
    def save_changes():
        updated_data = {
            "jmeno": entry_jmeno.get(),
            "prijmeni": entry_prijmeni.get(),
            "vek": int(entry_vek.get()),
            "telefon": entry_telefon.get()
        }
        print(f"✏️ PUT ID {person['id']}: {updated_data}")
        try:
            response = requests.put(f"{API_URL}/insured/{person['id']}", json=updated_data)
            response.raise_for_status()
            print(f"✅ Upraven pojištěenec ID {person['id']}")
            edit_window.destroy()
            show_insured()
        except requests.exceptions.RequestException as e:
            print("❌ PUT chyba:", e)

    edit_window = customtkinter.CTkToplevel(app)
    edit_window.title("Upravit pojištěnce")
    edit_window.geometry("300x250")

    entry_jmeno = customtkinter.CTkEntry(edit_window, placeholder_text="Jméno")
    entry_jmeno.insert(0, person['jmeno'])
    entry_jmeno.pack(pady=5)

    entry_prijmeni = customtkinter.CTkEntry(edit_window, placeholder_text="Příjmení")
    entry_prijmeni.insert(0, person['prijmeni'])
    entry_prijmeni.pack(pady=5)

    entry_vek = customtkinter.CTkEntry(edit_window, placeholder_text="Věk")
    entry_vek.insert(0, str(person['vek']))
    entry_vek.pack(pady=5)

    entry_telefon = customtkinter.CTkEntry(edit_window, placeholder_text="Telefon")
    entry_telefon.insert(0, person['telefon'])
    entry_telefon.pack(pady=5)

    btn_save = customtkinter.CTkButton(edit_window, text="Uložit změny", command=save_changes)
    btn_save.pack(pady=10)

def show_insured():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    try:
        response = requests.get(f"{API_URL}/insured")
        response.raise_for_status()
        insured_list = response.json()
        print("🔄 GET pojištěců")

        if insured_list:
            for person in insured_list:
                row = customtkinter.CTkFrame(scrollable_frame)
                row.pack(fill="x", pady=2, padx=5)

                text = f"ID {person['id']}: {person['jmeno']} {person['prijmeni']}, {person['vek']} let, Tel: {person['telefon']}"
                label = customtkinter.CTkLabel(row, text=text, anchor="w")
                label.pack(side="left", fill="x", expand=True)

                btn_delete = customtkinter.CTkButton(row, text="Smazat", width=70,
                     command=lambda pid=person['id']: delete_insured(pid))
                btn_delete.pack(side="right", padx=5)

                btn_edit = customtkinter.CTkButton(row, text="Upravit", width=70,
                                command=lambda p=person: edit_insured(p))
                btn_edit.pack(side="right", padx=5)


        else:
            label = customtkinter.CTkLabel(scrollable_frame, text="Žádní pojištěnci v databázi.")
            label.pack(pady=5)

    except requests.exceptions.RequestException as e:
        print("❌ GET chyba:", e)
        label = customtkinter.CTkLabel(scrollable_frame, text=f"Chyba: {e}")
        label.pack(pady=5)

def save_insured():
    first = entry_first.get()
    last = entry_last.get()
    age = entry_age.get()
    phone = entry_phone.get()

    if first and last and age.isdigit() and phone:
        data = {
            "jmeno": first,
            "prijmeni": last,
            "vek": int(age),
            "telefon": phone
        }
        print("🔄 POST:", data)
        try:
            response = requests.post(f"{API_URL}/insured", json=data)
            response.raise_for_status()
            entry_first.delete(0, "end")
            entry_last.delete(0, "end")
            entry_age.delete(0, "end")
            entry_phone.delete(0, "end")
            app.focus_set()
            show_insured()
        except requests.exceptions.RequestException as e:
            print("❌ POST chyba:", e)
    else:
        print("❌ Chyba: Neplatné nebo prázdné údaje.")

# GUI
app = customtkinter.CTk()
app.title("Pojišťovna")
app.geometry("500x600")

entry_first = customtkinter.CTkEntry(app, placeholder_text="Jméno")
entry_first.pack(pady=5)

entry_last = customtkinter.CTkEntry(app, placeholder_text="Příjmení")
entry_last.pack(pady=5)

entry_age = customtkinter.CTkEntry(app, placeholder_text="Věk")
entry_age.pack(pady=5)

entry_phone = customtkinter.CTkEntry(app, placeholder_text="Telefon")
entry_phone.pack(pady=5)

button_save = customtkinter.CTkButton(app, text="Uložit pojištěnce", command=save_insured)
button_save.pack(pady=10)

button_show = customtkinter.CTkButton(app, text="Zobrazit pojištěnce", command=show_insured)
button_show.pack(pady=5)

scrollable_frame = customtkinter.CTkScrollableFrame(app, height=300)
scrollable_frame.pack(fill="both", expand=True, pady=10, padx=10)

app.mainloop()