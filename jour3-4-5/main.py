import tkinter as tk

from database import Database
from product_repository import ProductRepository
from category_repository import CategoryRepository
from export_service import ExportService
from chart_service import ChartService
from dashboard import Dashboard


if __name__ == "__main__":
    db              = Database()
    product_repo    = ProductRepository(db)
    category_repo   = CategoryRepository(db)
    export_service  = ExportService(product_repo)
    chart_service   = ChartService(product_repo)

    root = tk.Tk()
    Dashboard(root, product_repo, category_repo, export_service, chart_service)
    root.mainloop()

    db.close()