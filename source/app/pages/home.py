import flet as ft
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import base64

plt.switch_backend('agg')

from .components.page_layer import page_layer
from .components.graphs import graphs

def create_plot(title="График") -> ft.Image:
    """Создает и возвращает график в виде ft.Image"""
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_alpha(0.0)  # Полностью прозрачный
    ax.patch.set_alpha(0.5)   # Полупрозрачный фон графика
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    line, = ax.plot(x, y)
    line.set_color('#4B8BBE')
    ax.set_title(title, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_facecolor('#F0F0F0')
    fig.patch.set_facecolor('#F0F0F0')
    
    buf = BytesIO()
    plt.savefig(
        buf, 
        format="png", 
        dpi=100, 
        bbox_inches='tight',
        transparent=False
    )
    buf.seek(0)
    plt.close(fig)
    
    return ft.Image(
        src_base64=base64.b64encode(buf.getvalue()).decode("utf-8"),
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        border_radius=15,
    )

def home_view(page: ft.Page):
    plot1 = create_plot("График 1")
    plot2 = create_plot("График 2")
    plot3 = create_plot("График 3")

    return ft.View(
        "/",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Column(
                    controls=[
                        graphs(page, plot1, plot2, plot3)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        ],
    )