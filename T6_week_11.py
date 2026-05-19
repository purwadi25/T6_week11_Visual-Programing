# ==================================================
# Nama  : Bagas
# NIM   : F1D02310115
# Kelas : Grup 15
# Tugas : T6 Week 11 - Post Manager REST API
# ==================================================

import tkinter as tk
from tkinter import ttk, messagebox
from unittest import result
import requests
import threading

API_URL = "https://api.pahrul.my.id/api/posts"


class PostManagerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Post Manager")
        self.root.geometry("1100x600")

        # =========================
        # MAIN FRAME
        # =========================
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # =========================
        # LEFT FRAME (TABLE)
        # =========================
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        # TABLE
        columns = ("ID", "Title", "Author", "Status")

        self.tree = ttk.Treeview(
            left_frame,
            columns=columns,
            show="headings",
            height=20
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)

        # event klik row tabel
        self.tree.bind(
        "<<TreeviewSelect>>",
        self.on_select_post)

        # =========================
        # RIGHT FRAME (DETAIL FORM)
        # =========================
        right_frame = ttk.LabelFrame(
            main_frame,
            text="Post Detail",
            padding=10
        )
        right_frame.pack(side="right", fill="y", padx=10)

        # TITLE
        ttk.Label(right_frame, text="Title").pack(anchor="w")
        self.title_entry = ttk.Entry(right_frame, width=40)
        self.title_entry.pack(fill="x", pady=5)

        # BODY
        ttk.Label(right_frame, text="Body").pack(anchor="w")
        self.body_text = tk.Text(right_frame, height=8, width=40)
        self.body_text.pack(fill="x", pady=5)

        # AUTHOR
        ttk.Label(right_frame, text="Author").pack(anchor="w")
        self.author_entry = ttk.Entry(right_frame)
        self.author_entry.pack(fill="x", pady=5)

        # SLUG
        ttk.Label(right_frame, text="Slug").pack(anchor="w")
        self.slug_entry = ttk.Entry(right_frame)
        self.slug_entry.pack(fill="x", pady=5)

        # STATUS
        ttk.Label(right_frame, text="Status").pack(anchor="w")

        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            right_frame,
            textvariable=self.status_var,
            values=["published", "draft"],
            state="readonly"
        )
        self.status_combo.pack(fill="x", pady=5)

        # =========================
        # BUTTONS
        # =========================
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=10)

        self.add_button = ttk.Button(
        button_frame,
        text="Tambah",
        command=self.start_add_post
        )

        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = ttk.Button(
            button_frame,
            text="Edit",
            state="disabled",
            command=self.start_edit_post
        )
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = ttk.Button(
            button_frame,
            text="Hapus",
            state="disabled",
            command=self.confirm_delete
        )
        self.delete_button.grid(row=0, column=2, padx=5)

        # =========================
        # STATUS BAR
        # =========================
        self.status_label = ttk.Label(
            root,
            text="Ready",
            relief="sunken",
            anchor="w"
        )
        self.status_label.pack(fill="x", side="bottom")

        # load posts pertama kali
        threading.Thread(
            target=self.load_posts,
            daemon=True
        ).start()

    # =========================
    # LOAD POSTS
    # =========================
    def load_posts(self):

        self.update_status("Loading posts...")

        try:
            response = requests.get(
                API_URL,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            posts = result.get("data", [])

            # update UI di main thread
            self.root.after(
                0,
                lambda: self.display_posts(posts)
            )

        except requests.exceptions.Timeout:
            self.show_error("Request timeout")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error")

        except requests.exceptions.RequestException as e:
            self.show_error(str(e))

        finally:
            self.update_status("Ready")

    # =========================
    # DISPLAY POSTS TO TABLE
    # =========================
    def display_posts(self, posts):

        # hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)

        # masukkan data baru
        for post in posts:

            self.tree.insert(
                "",
                "end",
                values=(
                    post.get("id"),
                    post.get("title"),
                    post.get("author"),
                    post.get("status")
                )
            )

    # =========================
    # UPDATE STATUS
    # =========================
    def update_status(self, message):

        self.root.after(
            0,
            lambda: self.status_label.config(text=message)
        )

     # =========================
    # SHOW ERROR
    # =========================
    def show_error(self, message):

        self.root.after(
            0,
            lambda: messagebox.showerror(
                "Error",
                message
            )
        )

    # =========================
    # SELECT POST
    # =========================
    def on_select_post(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        post_id = item["values"][0]

        # aktifkan tombol
        self.edit_button.config(state="normal")
        self.delete_button.config(state="normal")

        # load detail di thread
        threading.Thread(
            target=self.load_post_detail,
            args=(post_id,),
            daemon=True
        ).start()

        # =========================
    # LOAD DETAIL POST
    # =========================
    def load_post_detail(self, post_id):

        self.update_status("Loading detail...")

        try:

            response = requests.get(
                f"{API_URL}/{post_id}",
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            post = result.get("data", {})

            self.root.after(
                0,
                lambda: self.fill_form(post)
            )

        except requests.exceptions.Timeout:
            self.show_error("Request timeout")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error")

        except requests.exceptions.RequestException as e:
            self.show_error(str(e))

        finally:
            self.update_status("Ready")

    # =========================
    # FILL FORM
    # =========================
    def fill_form(self, post):

        self.selected_post_id = post.get("id")

        # title
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(
            0,
            post.get("title", "")
        )

        # body
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert(
            tk.END,
            post.get("body", "")
        )

        # author
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(
            0,
            post.get("author", "")
        )

        # slug
        self.slug_entry.delete(0, tk.END)
        self.slug_entry.insert(
            0,
            post.get("slug", "")
        )

        # status
        self.status_var.set(
            post.get("status", "")
        )

    # =========================
    # GET FORM DATA
    # =========================
    def get_form_data(self):

        return {
            "title": self.title_entry.get(),
            "body": self.body_text.get("1.0", tk.END).strip(),
            "author": self.author_entry.get(),
            "slug": self.slug_entry.get(),
            "status": self.status_var.get()
        }
    
    # =========================
    # START ADD POST
    # =========================
    def start_add_post(self):

        threading.Thread(
            target=self.add_post,
            daemon=True
        ).start()

    # =========================
    # ADD POST
    # =========================
    def add_post(self):

        data = self.get_form_data()

        # validasi field kosong
        if (
            not data["title"] or
            not data["body"] or
            not data["author"] or
            not data["slug"] or
            not data["status"]
        ):

            self.show_error("Semua field wajib diisi")
            return

        self.update_status("Adding post...")

        try:

            response = requests.post(
                API_URL,
                json=data,
                timeout=10
            )

            # slug duplicate
            if response.status_code == 422:

                self.show_error(
                    "Slug sudah digunakan"
                )

                return

            response.raise_for_status()

            result = response.json()

            post = result.get("data", {})

            post_id = post.get("id")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Sukses",
                    f"Post berhasil ditambahkan\nID: {post_id}"
                )
            )

            # refresh tabel
            self.load_posts()

            # clear form
            self.root.after(
                0,
                self.clear_form
            )

        except requests.exceptions.Timeout:
            self.show_error("Request timeout")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error")

        except requests.exceptions.RequestException as e:
            self.show_error(str(e))

        finally:
            self.update_status("Ready")

    # =========================
    # CLEAR FORM
    # =========================
    def clear_form(self):

        self.title_entry.delete(0, tk.END)

        self.body_text.delete(
            "1.0",
            tk.END
        )

        self.author_entry.delete(0, tk.END)

        self.slug_entry.delete(0, tk.END)

        self.status_var.set("")

        self.edit_button.config(
            state="disabled"
        )

        self.delete_button.config(
            state="disabled"
        )

    # =========================
    # CONFIRM DELETE
    # =========================
    def confirm_delete(self):

        if not hasattr(self, "selected_post_id"):
            return

        confirm = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus post ini?\nSemua comments juga akan terhapus."
        )

        if confirm:

            threading.Thread(
                target=self.delete_post,
                daemon=True
            ).start()

    # =========================
    # DELETE POST
    # =========================
    def delete_post(self):

        self.update_status("Deleting post...")

        try:

            response = requests.delete(
                f"{API_URL}/{self.selected_post_id}",
                timeout=10
            )

            response.raise_for_status()

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Sukses",
                    "Post berhasil dihapus"
                )
            )

            # refresh tabel
            self.load_posts()

            # clear form
            self.root.after(
                0,
                self.clear_form
            )

        except requests.exceptions.Timeout:
            self.show_error("Request timeout")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error")

        except requests.exceptions.RequestException as e:
            self.show_error(str(e))

        finally:
            self.update_status("Ready")

    # =========================
    # START EDIT POST
    # =========================
    def start_edit_post(self):

        threading.Thread(
            target=self.edit_post,
            daemon=True
        ).start()

    # =========================
    # EDIT POST
    # =========================
    def edit_post(self):

        if not hasattr(self, "selected_post_id"):
            return

        data = self.get_form_data()

        # validasi field kosong
        if (
            not data["title"] or
            not data["body"] or
            not data["author"] or
            not data["slug"] or
            not data["status"]
        ):

            self.show_error(
                "Semua field wajib diisi"
            )

            return

        self.update_status("Updating post...")

        try:

            response = requests.put(
                f"{API_URL}/{self.selected_post_id}",
                json=data,
                timeout=10
            )

            # slug duplicate
            if response.status_code == 422:

                self.show_error(
                    "Slug sudah digunakan"
                )

                return

            response.raise_for_status()

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Sukses",
                    "Post berhasil diupdate"
                )
            )

            # refresh tabel
            self.load_posts()

        except requests.exceptions.Timeout:
            self.show_error("Request timeout")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error")

        except requests.exceptions.RequestException as e:
            self.show_error(str(e))

        finally:
            self.update_status("Ready")


# =========================
# MAIN PROGRAM
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = PostManagerApp(root)
    root.mainloop()