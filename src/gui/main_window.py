from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import cv2

from src.core.crop_io import crop_image, load_image, save_image
from src.core.transform import rotate_image, zoom_image
from src.gui.widgets import ImageControls
from src.utils.helpers import cv_image_to_tk


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Image Viewer - Xử lý ảnh số")
        self.geometry("1280x760")
        self.minsize(980, 600)
        project_root = Path(__file__).resolve().parents[2]
        self.input_dir = project_root / "data" / "input"
        self.output_dir = project_root / "data" / "output"
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.input_files: list[Path] = []
        self.output_files: list[Path] = []
        self.original_image = None
        self.result_image = None
        self._tk_images: list[object] = []
        self._build_ui()
        self._refresh_file_lists(load_first=True)

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Mở ảnh ngoài", command=self.open_image).pack(
            side="left"
        )
        ttk.Button(toolbar, text="Lưu kết quả", command=self.save_result).pack(
            side="left", padx=8
        )
        self.file_label = ttk.Label(toolbar, text="Chưa mở ảnh")
        self.file_label.pack(side="left", padx=10)

        self.controls = ImageControls(self, self.apply_transformations, self.reset)
        self.controls.pack(fill="x", padx=10, pady=(0, 10))

        content = ttk.Frame(self, padding=(10, 0, 10, 10))
        content.pack(fill="both", expand=True)
        self._build_file_browser(content)

        views = ttk.Frame(content)
        views.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.before_panel = self._create_image_panel(views, "Before")
        self.before_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.after_panel = self._create_image_panel(views, "After")
        self.after_panel.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.bind("<Configure>", lambda _event: self._refresh_images())

    def _build_file_browser(self, parent: tk.Misc) -> None:
        browser = ttk.Frame(parent, width=220)
        browser.pack(side="left", fill="y")
        browser.pack_propagate(False)

        input_group = ttk.LabelFrame(browser, text="Ảnh trong input", padding=6)
        input_group.pack(fill="both", expand=True)
        self.input_list = tk.Listbox(input_group, exportselection=False)
        self.input_list.pack(side="left", fill="both", expand=True)
        input_scroll = ttk.Scrollbar(
            input_group, orient="vertical", command=self.input_list.yview
        )
        input_scroll.pack(side="right", fill="y")
        self.input_list.configure(yscrollcommand=input_scroll.set)
        self.input_list.bind("<<ListboxSelect>>", self._on_input_selected)

        output_group = ttk.LabelFrame(browser, text="Ảnh trong output", padding=6)
        output_group.pack(fill="both", expand=True, pady=(10, 0))
        self.output_list = tk.Listbox(output_group, exportselection=False)
        self.output_list.pack(side="left", fill="both", expand=True)
        output_scroll = ttk.Scrollbar(
            output_group, orient="vertical", command=self.output_list.yview
        )
        output_scroll.pack(side="right", fill="y")
        self.output_list.configure(yscrollcommand=output_scroll.set)
        self.output_list.bind("<Double-Button-1>", self._on_output_selected)

    def _refresh_file_lists(self, load_first: bool = False) -> None:
        extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
        self.input_files = sorted(
            (
                path
                for path in self.input_dir.iterdir()
                if path.suffix.lower() in extensions
            ),
            key=lambda path: path.name.lower(),
        )
        self.output_files = sorted(
            (
                path
                for path in self.output_dir.iterdir()
                if path.suffix.lower() in extensions
            ),
            key=lambda path: path.name.lower(),
        )
        self.input_list.delete(0, tk.END)
        for path in self.input_files:
            self.input_list.insert(tk.END, path.name)
        self.output_list.delete(0, tk.END)
        for path in self.output_files:
            self.output_list.insert(tk.END, path.name)
        if load_first and self.input_files:
            self.input_list.selection_set(0)
            self.input_list.activate(0)
            self._load_image(self.input_files[0])

    def _on_input_selected(self, _event: tk.Event) -> None:
        selection = self.input_list.curselection()
        if selection:
            self._load_image(self.input_files[selection[0]])

    def _on_output_selected(self, _event: tk.Event) -> None:
        selection = self.output_list.curselection()
        if selection:
            self._load_image(self.output_files[selection[0]], reset_controls=False)

    def _load_image(self, file_path: Path, reset_controls: bool = True) -> None:
        try:
            image = load_image(file_path)
        except ValueError:
            messagebox.showerror("Lỗi", f"Không thể đọc ảnh: {file_path.name}")
            return
        self.original_image = image
        self.result_image = image.copy()
        self.file_label.configure(text=file_path.name)
        if reset_controls:
            self.controls.zoom_var.set(1.0)
            self.controls.rotate_var.set(0.0)
            self._reset_crop_defaults()
        self._refresh_images()

    def _create_image_panel(self, parent: tk.Misc, title: str) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=title, padding=8)
        frame.pack_propagate(False)
        frame.configure(width=520, height=500)
        label = ttk.Label(frame, text="Chưa có ảnh", anchor="center")
        label.pack(fill="both", expand=True)
        frame.image_label = label
        return frame

    def open_image(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            initialdir=str(self.input_dir),
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return
        self._load_image(Path(file_path))

    def apply_transformations(self) -> None:
        if self.original_image is None:
            messagebox.showinfo("Thông báo", "Hãy mở một ảnh trước.")
            return
        try:
            controls = self.controls
            result = zoom_image(self.original_image, controls.zoom_var.get())
            result = rotate_image(result, controls.rotate_var.get())
            crop_width = controls.crop_w_var.get()
            crop_height = controls.crop_h_var.get()
            if crop_width or crop_height:
                result = crop_image(
                    result,
                    controls.crop_x_var.get(),
                    controls.crop_y_var.get(),
                    crop_width,
                    crop_height,
                )
            self.result_image = result
            self._refresh_images()
        except (TypeError, ValueError, cv2.error) as error:
            messagebox.showerror("Tham số không hợp lệ", str(error))

    def save_result(self) -> None:
        if self.result_image is None:
            messagebox.showinfo("Thông báo", "Chưa có ảnh kết quả để lưu.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Lưu ảnh kết quả",
            initialdir=str(self.output_dir),
            initialfile=f"{Path(self.file_label.cget('text')).stem}_result.png",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")],
        )
        if not file_path:
            return
        if not save_image(self.result_image, file_path):
            messagebox.showerror("Lỗi", "Không thể lưu ảnh kết quả.")
            return
        self._refresh_file_lists()
        saved_path = Path(file_path)
        if saved_path.parent.resolve() == self.output_dir.resolve():
            self._select_output_file(saved_path)

    def _select_output_file(self, file_path: Path) -> None:
        for index, output_file in enumerate(self.output_files):
            if output_file.resolve() == file_path.resolve():
                self.output_list.selection_clear(0, tk.END)
                self.output_list.selection_set(index)
                self.output_list.activate(index)
                self.output_list.see(index)
                break

    def reset(self) -> None:
        if self.original_image is None:
            return
        self.result_image = self.original_image.copy()
        self.controls.zoom_var.set(1.0)
        self.controls.rotate_var.set(0.0)
        self._reset_crop_defaults()
        self._refresh_images()

    def _reset_crop_defaults(self) -> None:
        self.controls.crop_x_var.set(0)
        self.controls.crop_y_var.set(0)
        self.controls.crop_w_var.set(0)
        self.controls.crop_h_var.set(0)

    def _refresh_images(self) -> None:
        if self.original_image is None or self.result_image is None:
            return
        self._tk_images = [
            cv_image_to_tk(self.original_image, self._panel_size(self.before_panel)),
            cv_image_to_tk(self.result_image, self._panel_size(self.after_panel)),
        ]
        self.before_panel.image_label.configure(image=self._tk_images[0], text="")
        self.after_panel.image_label.configure(image=self._tk_images[1], text="")

    @staticmethod
    def _panel_size(panel: ttk.LabelFrame) -> tuple[int, int]:
        return (max(panel.winfo_width() - 16, 100), max(panel.winfo_height() - 16, 100))
