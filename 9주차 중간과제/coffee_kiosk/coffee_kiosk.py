"""커피매장 주문 키오스크 - tkinter 실습 과제."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# 메뉴와 추가 금액을 한 곳에 모아 두었습니다.
MENUS = {
    '커피': [('아메리카노', 2500, 'americano.png'),
           ('카페라떼', 3500, 'latte.png')],
    '차': [('홍차', 3000, 'black_tea.png'),
          ('녹차', 3000, 'green_tea.png')],
}
TEMPERATURE_PRICE = {'HOT': 0, 'ICE': 500}
SIZE_PRICE = {'Small (355mL)': 0, 'Medium (473mL)': 500,
              'Large (591mL)': 1000}
OPTION_PRICE = {'샷 추가': 500, '시럽 추가': 300}
IMAGE_DIR = Path(__file__).resolve().parent / 'images'


def calculate_price(base_price, temperature, size, shot=False, syrup=False):
    """음료 한 잔의 가격을 정수(원)로 계산합니다."""
    return (base_price + TEMPERATURE_PRICE[temperature] + SIZE_PRICE[size]
            + OPTION_PRICE['샷 추가'] * bool(shot)
            + OPTION_PRICE['시럽 추가'] * bool(syrup))


class CoffeeKiosk:
    def __init__(self, root):
        self.root = root
        self.root.title('커피매장 주문 키오스크')
        self.root.geometry('1080x700')
        self.root.minsize(1080, 700)
        self.root.configure(bg='#f4f1eb')
        self.cart = []
        self.order_number = 1  # 프로그램을 실행하는 동안 순서대로 증가합니다.
        self.photos = {}       # 사진이 화면에서 사라지지 않도록 참조를 보관합니다.
        self.menu_buttons = {}
        self.selected_name = ''
        self.base_price = 0
        self.category = '커피'
        self.temperature = tk.StringVar(value='HOT')
        self.size = tk.StringVar(value=next(iter(SIZE_PRICE)))
        self.shot = tk.BooleanVar(value=False)
        self.syrup = tk.BooleanVar(value=False)
        self.quantity = tk.StringVar(value='1')
        self.selected_text = tk.StringVar()
        self.price_text = tk.StringVar()
        self.total_text = tk.StringVar(value='총 결제 금액: 0원')
        self.order_text = tk.StringVar(value='다음 주문번호: 001')
        self.make_widgets()
        self.select_menu('커피', MENUS['커피'][0])

    def make_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('맑은 고딕', 12), padding=(24, 8))
        style.configure('Treeview', font=('맑은 고딕', 10), rowheight=32)
        style.configure('Treeview.Heading', font=('맑은 고딕', 10, 'bold'))
        tk.Label(self.root, text='오늘의 커피', bg='#334c40', fg='white',
                 font=('맑은 고딕', 23, 'bold'), pady=10).pack(fill='x')
        tk.Label(self.root, text='메뉴 선택 → 옵션 선택 → 주문 담기 → 결제하기',
                 bg='#f4f1eb', font=('맑은 고딕', 11), pady=7).pack()

        body = tk.Frame(self.root, bg='#f4f1eb')
        body.pack(fill='both', expand=True, padx=16, pady=(0, 12))
        body.columnconfigure(0, weight=1, uniform='panel')
        body.columnconfigure(1, weight=1, uniform='panel')
        body.rowconfigure(0, weight=1)
        left = tk.Frame(body, bg='#f4f1eb')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        right = tk.Frame(body, bg='#f4f1eb')
        right.grid(row=0, column=1, sticky='nsew', padx=(8, 0))

        self.notebook = ttk.Notebook(left)
        self.notebook.pack(fill='x')
        self.tab_categories = []
        for category, menus in MENUS.items():
            tab = tk.Frame(self.notebook, bg='white')
            self.notebook.add(tab, text=category)
            self.tab_categories.append(category)
            for column, menu in enumerate(menus):
                name, price, filename = menu
                path = IMAGE_DIR / filename
                # 필수 사진이 없으면 빈 그림으로 대신하지 않고 오류를 안내합니다.
                self.photos[name] = tk.PhotoImage(file=str(path))
                button = tk.Button(
                    tab, text=f'{name}\n{price:,}원', image=self.photos[name],
                    compound='top', font=('맑은 고딕', 12), bg='white',
                    relief='solid', bd=1, cursor='hand2', padx=2, pady=5,
                    command=lambda c=category, m=menu: self.select_menu(c, m))
                button.grid(row=0, column=column, padx=5, pady=7, sticky='ew')
                tab.columnconfigure(column, weight=1)
                self.menu_buttons[name] = button
        self.notebook.bind('<<NotebookTabChanged>>', self.change_tab)

        box = tk.LabelFrame(left, text='선택한 음료 / 옵션', bg='white',
                            font=('맑은 고딕', 11, 'bold'), padx=10, pady=5)
        box.pack(fill='both', expand=True, pady=(10, 0))
        tk.Label(box, textvariable=self.selected_text, bg='white',
                 font=('맑은 고딕', 13, 'bold')).pack(anchor='w')
        row = tk.Frame(box, bg='white')
        row.pack(fill='x', pady=4)
        tk.Label(row, text='온도  ', bg='white').pack(side='left')
        for name, extra in TEMPERATURE_PRICE.items():
            tk.Radiobutton(row, text=f'{name} (+{extra:,}원)',
                           variable=self.temperature, value=name, bg='white',
                           command=self.update_price).pack(side='left', padx=5)
        row = tk.Frame(box, bg='white')
        row.pack(fill='x', pady=4)
        tk.Label(row, text='용량  ', bg='white').pack(side='left')
        combo = ttk.Combobox(row, textvariable=self.size,
                             values=list(SIZE_PRICE), state='readonly', width=20)
        combo.pack(side='left')
        combo.bind('<<ComboboxSelected>>', lambda e: self.update_price())
        tk.Label(row, text=' M +500원 / L +1,000원', bg='white').pack(side='left')
        row = tk.Frame(box, bg='white')
        row.pack(fill='x', pady=4)
        self.shot_button = tk.Checkbutton(row, text='샷 추가 (+500원 / 커피만)',
                                         variable=self.shot, bg='white',
                                         command=self.update_price)
        self.shot_button.pack(side='left')
        tk.Checkbutton(row, text='시럽 추가 (+300원)', variable=self.syrup,
                       bg='white', command=self.update_price).pack(side='left')
        row = tk.Frame(box, bg='white')
        row.pack(fill='x', pady=4)
        tk.Label(row, text='수량  ', bg='white').pack(side='left')
        combo = ttk.Combobox(row, textvariable=self.quantity,
                             values=[str(i) for i in range(1, 11)],
                             state='readonly', width=5)
        combo.pack(side='left')
        combo.bind('<<ComboboxSelected>>', lambda e: self.update_price())
        tk.Label(box, textvariable=self.price_text, bg='white', fg='#23513a',
                 font=('맑은 고딕', 13, 'bold')).pack(anchor='w', pady=5)
        tk.Button(box, text='주문 담기', bg='#334c40', fg='white',
                  font=('맑은 고딕', 12, 'bold'), command=self.add_to_cart,
                  pady=7).pack(fill='x', pady=(0, 3))

        tk.Label(right, text='주문 내역', bg='#f4f1eb',
                 font=('맑은 고딕', 15, 'bold')).pack(anchor='w')
        table_frame = tk.Frame(right)
        table_frame.pack(fill='x', pady=7)
        self.table = ttk.Treeview(table_frame, columns=('name', 'option', 'qty', 'sum'),
                                  show='headings', height=6, selectmode='browse')
        for key, title, width in [('name', '메뉴', 95), ('option', '온도 / 용량 / 옵션', 225),
                                  ('qty', '수량', 38), ('sum', '금액', 85)]:
            self.table.heading(key, text=title)
            self.table.column(key, width=width, minwidth=width, stretch=False,
                              anchor='center')
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        row = tk.Frame(right, bg='#f4f1eb')
        row.pack(fill='x')
        tk.Button(row, text='선택 삭제', command=self.remove_selected).pack(side='left')
        tk.Button(row, text='전체 비우기', command=self.clear_cart).pack(side='left', padx=6)
        tk.Label(right, textvariable=self.total_text, bg='#f4f1eb', fg='#23513a',
                 font=('맑은 고딕', 18, 'bold')).pack(anchor='e', pady=(12, 3))
        tk.Label(right, textvariable=self.order_text, bg='#f4f1eb',
                 font=('맑은 고딕', 11)).pack(anchor='e')
        tk.Button(right, text='결제하기 (모의 결제)', command=self.pay,
                  bg='#bf7540', fg='white', font=('맑은 고딕', 13, 'bold'),
                  pady=9).pack(fill='x', pady=7)
        tk.Label(right, text='최근 주문 영수증', bg='#f4f1eb',
                 font=('맑은 고딕', 11, 'bold')).pack(anchor='w')
        self.receipt = tk.Text(right, height=8, font=('맑은 고딕', 10),
                               wrap='word', state='disabled', bg='white')
        self.receipt.pack(fill='both', expand=True, pady=(5, 0))

    def change_tab(self, event):
        category = self.tab_categories[self.notebook.index('current')]
        self.select_menu(category, MENUS[category][0])

    def select_menu(self, category, menu):
        self.category = category
        self.selected_name, self.base_price, _ = menu
        # 메뉴 변경 시 이전 음료의 옵션이 남지 않도록 초기화합니다.
        self.temperature.set('HOT')
        self.size.set(next(iter(SIZE_PRICE)))
        self.shot.set(False)
        self.syrup.set(False)
        self.quantity.set('1')
        self.shot_button.config(state='normal' if category == '커피' else 'disabled')
        for name, button in self.menu_buttons.items():
            button.config(bg='#dce9df' if name == self.selected_name else 'white')
        self.selected_text.set(f'{self.selected_name}  /  기본 {self.base_price:,}원')
        self.update_price()

    def current_item(self):
        quantity = int(self.quantity.get())
        if not 1 <= quantity <= 10:
            raise ValueError('수량은 1~10 사이여야 합니다.')
        shot = self.shot.get() and self.category == '커피'
        options = []
        if shot:
            options.append('샷')
        if self.syrup.get():
            options.append('시럽')
        size = self.size.get()
        unit_price = calculate_price(self.base_price, self.temperature.get(), size,
                                     shot, self.syrup.get())
        description = f'{self.temperature.get()} / {size.split()[0]}'
        if options:
            description += ' / ' + '+'.join(options)
        return {'name': self.selected_name, 'description': description,
                'quantity': quantity, 'unit_price': unit_price}

    def update_price(self):
        item = self.current_item()
        subtotal = item['unit_price'] * item['quantity']
        self.price_text.set(f"1잔 {item['unit_price']:,}원 × {item['quantity']}잔 = {subtotal:,}원")

    def add_to_cart(self):
        item = self.current_item()
        # 선택값을 별도 딕셔너리로 저장해 이후 옵션 변경의 영향을 받지 않습니다.
        self.cart.append(item)
        self.refresh_cart()

    def refresh_cart(self):
        for item_id in self.table.get_children():
            self.table.delete(item_id)
        for index, item in enumerate(self.cart):
            subtotal = item['unit_price'] * item['quantity']
            self.table.insert('', 'end', iid=str(index), values=(
                item['name'], item['description'], item['quantity'], f'{subtotal:,}원'))
        self.total_text.set(f'총 결제 금액: {self.cart_total():,}원')

    def cart_total(self):
        return sum(item['unit_price'] * item['quantity'] for item in self.cart)

    def remove_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo('삭제 안내', '삭제할 주문을 먼저 선택해주세요.')
            return
        del self.cart[int(selected[0])]
        self.refresh_cart()

    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart()

    def pay(self):
        if not self.cart:
            messagebox.showwarning('주문 확인', '음료를 먼저 주문에 담아주세요.')
            return
        total = self.cart_total()
        if not messagebox.askyesno('결제 확인', f'{total:,}원을 모의 결제하시겠습니까?'):
            return
        lines = [f'주문번호: {self.order_number:03d}', '결제가 완료되었습니다. (모의 결제)']
        for item in self.cart:
            lines.append(f"{item['name']}  {item['description']}")
            lines.append(f"  {item['unit_price']:,}원 × {item['quantity']}잔 = "
                         f"{item['unit_price'] * item['quantity']:,}원")
        lines.append(f'총 결제 금액: {total:,}원')
        self.receipt.config(state='normal')
        self.receipt.delete('1.0', 'end')
        self.receipt.insert('1.0', '\n'.join(lines))
        self.receipt.config(state='disabled')
        completed_number = self.order_number
        self.order_number += 1
        self.order_text.set(f'다음 주문번호: {self.order_number:03d}')
        self.clear_cart()
        messagebox.showinfo('주문 완료', f'주문번호: {completed_number:03d}\n'
                            f'결제 금액: {total:,}원\n오른쪽 영수증을 확인해주세요.')


def main():
    root = tk.Tk()
    try:
        CoffeeKiosk(root)
    except tk.TclError as error:
        messagebox.showerror('실행 오류', '사진 파일 또는 Tk 설정을 확인해주세요.\n'
                             '압축을 모두 푼 뒤 images 폴더와 함께 실행해야 합니다.\n\n'
                             + str(error))
        root.destroy()
        return
    root.mainloop()


if __name__ == '__main__':
    main()
