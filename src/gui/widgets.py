from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class ImageControls(ttk.LabelFrame):
    """Controls for geometric transforms and crop coordinates."""

    def __init__(
        self,
        parent: tk.Misc,
        on_apply: Callable[[], None],
        on_reset: Callable[[], None],
    ) -> None:
        super().__init__(parent, text="Điều khiển", padding=12)
        self.zoom_var = tk.DoubleVar(value=1.0)
        self.rotate_var = tk.DoubleVar(value=0.0)
        self.crop_x_var = tk.IntVar(value=0)
        self.crop_y_var = tk.IntVar(value=0)
        self.crop_w_var = tk.IntVar(value=0)
        self.crop_h_var = tk.IntVar(value=0)

        self._add_scale("Zoom", self.zoom_var, 0.1, 3.0, 0, on_apply)
        self._add_scale("Rotate", self.rotate_var, -180.0, 180.0, 1, on_apply)

        crop_frame = ttk.Frame(self)
        crop_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        for column, (label, variable) in enumerate(
            (
                ("X", self.crop_x_var),
                ("Y", self.crop_y_var),
                ("W", self.crop_w_var),
                ("H", self.crop_h_var),
            )
        ):
            ttk.Label(crop_frame, text=label).grid(row=0, column=column, padx=3)
            ttk.Entry(crop_frame, textvariable=variable, width=6).grid(
                row=1, column=column, padx=3
            )

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(button_frame, text="Áp dụng Crop", command=on_apply).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(button_frame, text="Đặt lại", command=on_reset).pack(side="left")

    def _add_scale(
        self,
        label: str,
        variable: tk.DoubleVar,
        minimum: float,
        maximum: float,
        row: int,
        on_change: Callable[[], None],
    ) -> None:
        ttk.Label(self, text=label).grid(row=row, column=0, sticky="w")
        ttk.Scale(
            self,
            from_=minimum,
            to=maximum,
            variable=variable,
            orient="horizontal",
            command=lambda _value: on_change(),
        ).grid(row=row, column=1, sticky="ew", padx=8)
        ttk.Entry(self, textvariable=variable, width=8).grid(row=row, column=2)
        self.columnconfigure(1, weight=1)
