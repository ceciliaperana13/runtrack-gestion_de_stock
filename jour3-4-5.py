import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import matplotlib.pyplot as plt

# CONNEXION
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Camboui2803",
    database="store"
)

cursor = connection.cursor()

# FONCTIONS DB

def get_categories():
    cursor.execute("SELECT id, name FROM category")
    return cursor.fetchall()

def get_products(category_id=None):
    if category_id:
        cursor.execute("""
            SELECT product.id, product.name, product.price, product.quantity, category.name
            FROM product
            JOIN category ON product.id_category = category.id
            WHERE category.id = %s
        """, (category_id,))
    else:
        cursor.execute("""
            SELECT product.id, product.name, product.price, product.quantity, category.name
            FROM product
            JOIN category ON product.id_category = category.id
        """)
    return cursor.fetchall()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for product in get_products():
        tree.insert("", tk.END, values=product)

def get_selected_category_id():
    selected = category_combo.get()
    for cat_id, cat_name in categories:
        if cat_name == selected:
            return cat_id
    return None

def add_product():
    try:
        nom = name_entry.get().strip()
        desc = desc_entry.get().strip()
        prix = price_entry.get().strip()
        quantite = quantity_entry.get().strip()
        cat_id = get_selected_category_id()

        if not nom or not prix or not quantite or not cat_id:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires (Nom, Prix, Quantité, Catégorie)")
            return

        cursor.execute("""
            INSERT INTO product (name, description, price, quantity, id_category)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, desc, int(prix), int(quantite), cat_id))
        connection.commit()
        refresh_table()
        messagebox.showinfo("Succès", "Produit ajouté !")
    except ValueError:
        messagebox.showerror("Erreur", "Prix et Quantité doivent être des nombres entiers")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def delete_product():
    try:
        selected = tree.focus()
        values = tree.item(selected, 'values')
        if not values:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit dans le tableau")
            return
        cursor.execute("DELETE FROM product WHERE id=%s", (values[0],))
        connection.commit()
        refresh_table()
        messagebox.showinfo("Succès", "Produit supprimé !")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def update_product():
    try:
        selected = tree.focus()
        values = tree.item(selected, 'values')
        if not values:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit dans le tableau")
            return
        prix = price_entry.get().strip()
        quantite = quantity_entry.get().strip()
        if not prix or not quantite:
            messagebox.showerror("Erreur", "Veuillez remplir Prix et Quantité pour modifier")
            return
        cursor.execute("""
            UPDATE product
            SET price=%s, quantity=%s
            WHERE id=%s
        """, (int(prix), int(quantite), values[0]))
        connection.commit()
        refresh_table()
        messagebox.showinfo("Succès", "Produit modifié !")
    except ValueError:
        messagebox.showerror("Erreur", "Prix et Quantité doivent être des nombres entiers")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def on_tree_select(event):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    if values:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        price_entry.delete(0, tk.END)
        price_entry.insert(0, values[2])
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[3])
        category_combo.set(values[4])

def export_csv():
    try:
        products = get_products()
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return
        with open(file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity", "Category"])
            writer.writerows(products)
        messagebox.showinfo("Succès", "Export CSV réussi !")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def show_graph():
    cursor.execute("SELECT name, quantity FROM product")
    data = cursor.fetchall()
    names = [x[0] for x in data]
    quantities = [x[1] for x in data]
    plt.bar(names, quantities)
    plt.title("Stock par produit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# INTERFACE
root = tk.Tk()
root.title("Store Dashboard")
root.geometry("900x600")

tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Quantity", "Category"), show="headings")
for col in ("ID", "Name", "Price", "Quantity", "Category"):
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nom *").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Description").grid(row=1, column=0, sticky="e")
desc_entry = tk.Entry(frame)
desc_entry.grid(row=1, column=1)

tk.Label(frame, text="Prix *").grid(row=2, column=0, sticky="e")
price_entry = tk.Entry(frame)
price_entry.grid(row=2, column=1)

tk.Label(frame, text="Quantité *").grid(row=3, column=0, sticky="e")
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=3, column=1)

# Menu déroulant pour les catégories
categories = get_categories()
category_names = [cat[1] for cat in categories]

tk.Label(frame, text="Catégorie *").grid(row=4, column=0, sticky="e")
category_combo = ttk.Combobox(frame, values=category_names, state="readonly")
category_combo.grid(row=4, column=1)
if category_names:
    category_combo.set(category_names[0])

tk.Button(frame, text="Ajouter", command=add_product, bg="#4CAF50", fg="white").grid(row=5, column=0, pady=5)
tk.Button(frame, text="Modifier", command=update_product, bg="#2196F3", fg="white").grid(row=5, column=1)
tk.Button(frame, text="Supprimer", command=delete_product, bg="#f44336", fg="white").grid(row=6, column=0)
tk.Button(frame, text="Exporter CSV", command=export_csv).grid(row=6, column=1)
tk.Button(frame, text="Graphique", command=show_graph).grid(row=7, column=0)

refresh_table()
root.mainloop()