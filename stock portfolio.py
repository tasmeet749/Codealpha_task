import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, json
from datetime import datetime
from collections import defaultdict

# Stock data with prices
STOCKS = {"AAPL": 180.25, "TSLA": 250.50, "GOOGL": 140.75, "MSFT": 380.90, 
          "AMZN": 145.30, "META": 320.45, "NVDA": 450.60, "JPM": 155.20, "V": 260.80, "WMT": 165.40}

class PortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("1000x700")
        
        self.portfolio = {}
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_portfolio)
        file_menu.add_command(label="Load", command=self.load_portfolio)
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Input & Portfolio
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Input section
        input_frame = ttk.LabelFrame(left_frame, text="Add Stock", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Stock:").grid(row=0, column=0, sticky=tk.W)
        self.stock_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.stock_var, values=list(STOCKS.keys()), 
                     width=10, state='readonly').grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.qty_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.qty_var, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Price:").grid(row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.price_label = ttk.Label(input_frame, text="$0.00")
        self.price_label.grid(row=0, column=5, padx=5)
        
        ttk.Button(input_frame, text="Add", command=self.add_stock).grid(row=0, column=6, padx=10)
        ttk.Button(input_frame, text="Remove", command=self.remove_stock).grid(row=0, column=7)
        
        self.stock_var.trace('w', self.update_price)
        
        # Portfolio table
        table_frame = ttk.LabelFrame(left_frame, text="Portfolio", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Ticker', 'Quantity', 'Avg Cost', 'Current Price', 'Value', 'Gain/Loss', '%')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.E if col != 'Ticker' else tk.W)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Analytics
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Summary
        summary_frame = ttk.LabelFrame(right_frame, text="Portfolio Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_text = tk.Text(summary_frame, height=8, width=40, font=('Courier', 10))
        self.summary_text.pack(fill=tk.X)
        
        # Distribution
        dist_frame = ttk.LabelFrame(right_frame, text="Distribution", padding=10)
        dist_frame.pack(fill=tk.BOTH, expand=True)
        
        self.dist_text = tk.Text(dist_frame, height=15, width=40, font=('Courier', 10))
        self.dist_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X, side=tk.BOTTOM)
    
    def update_price(self, *args):
        ticker = self.stock_var.get()
        if ticker in STOCKS:
            self.price_label.config(text=f"${STOCKS[ticker]:.2f}")
    
    def add_stock(self):
        ticker = self.stock_var.get().upper()
        qty = self.qty_var.get()
        
        if not ticker or ticker not in STOCKS:
            messagebox.showerror("Error", "Select valid stock")
            return
        
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid quantity")
            return
        
        price = STOCKS[ticker]
        if ticker in self.portfolio:
            old = self.portfolio[ticker]
            self.portfolio[ticker] = {
                'qty': old['qty'] + qty,
                'total_cost': old['total_cost'] + (qty * price),
                'avg_cost': (old['total_cost'] + (qty * price)) / (old['qty'] + qty)
            }
        else:
            self.portfolio[ticker] = {
                'qty': qty,
                'total_cost': qty * price,
                'avg_cost': price
            }
        
        self.stock_var.set("")
        self.qty_var.set("")
        self.update_display()
        self.status_var.set(f"Added {qty} shares of {ticker}")
    
    def remove_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select stock to remove")
            return
        
        ticker = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Remove {ticker}?"):
            del self.portfolio[ticker]
            self.update_display()
            self.status_var.set(f"Removed {ticker}")
    
    def update_display(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_value = 0
        total_cost = 0
        
        # Update portfolio table
        for ticker, data in self.portfolio.items():
            current_price = STOCKS[ticker]
            value = data['qty'] * current_price
            gain_loss = value - data['total_cost']
            pct_change = (gain_loss / data['total_cost'] * 100) if data['total_cost'] > 0 else 0
            
            self.tree.insert('', tk.END, values=(
                ticker,
                data['qty'],
                f"${data['avg_cost']:.2f}",
                f"${current_price:.2f}",
                f"${value:.2f}",
                f"${gain_loss:.2f}",
                f"{pct_change:.1f}%"
            ))
            
            total_value += value
            total_cost += data['total_cost']
        
        # Update summary
        self.summary_text.delete(1.0, tk.END)
        summary = f"Portfolio Value: ${total_value:,.2f}\n"
        summary += f"Total Cost:     ${total_cost:,.2f}\n"
        summary += f"Gain/Loss:      ${total_value - total_cost:,.2f}\n"
        summary += f"Return:         {((total_value - total_cost) / total_cost * 100):.1f}%\n"
        summary += f"Stocks:         {len(self.portfolio)}\n"
        
        if self.portfolio:
            best = max(self.portfolio.items(), key=lambda x: (STOCKS[x[0]] - x[1]['avg_cost']) / x[1]['avg_cost'])
            worst = min(self.portfolio.items(), key=lambda x: (STOCKS[x[0]] - x[1]['avg_cost']) / x[1]['avg_cost'])
            summary += f"Best:          {best[0]} (+{((STOCKS[best[0]] - best[1]['avg_cost']) / best[1]['avg_cost'] * 100):.1f}%)\n"
            summary += f"Worst:         {worst[0]} ({((STOCKS[worst[0]] - worst[1]['avg_cost']) / worst[1]['avg_cost'] * 100):.1f}%)"
        
        self.summary_text.insert(tk.END, summary)
        
        # Update distribution
        self.dist_text.delete(1.0, tk.END)
        if self.portfolio:
            self.dist_text.insert(tk.END, "PORTFOLIO DISTRIBUTION\n" + "="*30 + "\n\n")
            for ticker, data in sorted(self.portfolio.items(), key=lambda x: x[1]['qty'] * STOCKS[x[0]], reverse=True):
                value = data['qty'] * STOCKS[ticker]
                pct = (value / total_value * 100) if total_value > 0 else 0
                bar = "█" * int(pct/2) + "░" * (50 - int(pct/2))
                self.dist_text.insert(tk.END, f"{ticker:<6} {bar} {pct:5.1f}% (${value:,.2f})\n")
    
    def save_portfolio(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", 
                                               filetypes=[("JSON", "*.json")])
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.portfolio, f)
            self.status_var.set(f"Saved to {filename}")
    
    def load_portfolio(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                self.portfolio = json.load(f)
            self.update_display()
            self.status_var.set(f"Loaded from {filename}")
    
    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", 
                                               filetypes=[("CSV", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Ticker', 'Quantity', 'Avg Cost', 'Current Price', 'Value', 'Gain/Loss'])
                for ticker, data in self.portfolio.items():
                    price = STOCKS[ticker]
                    value = data['qty'] * price
                    gain_loss = value - data['total_cost']
                    writer.writerow([ticker, data['qty'], f"${data['avg_cost']:.2f}", 
                                   f"${price:.2f}", f"${value:.2f}", f"${gain_loss:.2f}"])
            self.status_var.set(f"Exported to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()