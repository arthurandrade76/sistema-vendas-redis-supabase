import tkinter as tk
from tkinter import ttk, messagebox
import banco

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Simples — Supabase & Redis")
        self.geometry("800x520")
        self.configure(bg="#F3F4F6")

        self.modo_atual = "produtos"

        self._criar_interface()
        self.carregar_dados()

    def _criar_interface(self):
        self.frame_topo = tk.Frame(self, bg="#1F2937", pady=10)
        self.frame_topo.pack(fill="x")

        self.lbl_fonte = tk.Label(
            self.frame_topo,
            text="Fonte: Aguardando consulta...",
            font=("Arial", 12, "bold"),
            fg="#60A5FA",
            bg="#1F2937"
        )
        self.lbl_fonte.pack()

        self.frame_botoes = tk.Frame(self, bg="#F3F4F6", pady=10)
        self.frame_botoes.pack(fill="x", padx=15)

        tk.Button(
            self.frame_botoes, text="📦 Ver Produtos", bg="#3B82F6", fg="white",
            font=("Arial", 10, "bold"), padx=10, pady=5, command=self._ver_produtos
        ).pack(side="left", padx=5)

        tk.Button(
            self.frame_botoes, text="👥 Ver Clientes", bg="#6B7280", fg="white",
            font=("Arial", 10, "bold"), padx=10, pady=5, command=self._ver_clientes
        ).pack(side="left", padx=5)

        tk.Button(
            self.frame_botoes, text="🔄 Recarregar", bg="#10B981", fg="white",
            font=("Arial", 10, "bold"), padx=10, pady=5, command=self.carregar_dados
        ).pack(side="left", padx=5)

        tk.Button(
            self.frame_botoes, text="🧹 Limpar Cache Redis", bg="#EF4444", fg="white",
            font=("Arial", 10, "bold"), padx=10, pady=5, command=self._limpar_cache
        ).pack(side="right", padx=5)

        self.frame_tabela = tk.Frame(self, bg="#F3F4F6")
        self.frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

        self.tabela = ttk.Treeview(self.frame_tabela, columns=("c1", "c2", "c3", "c4"), show="headings", height=10)
        self.tabela.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        self.frame_form = tk.LabelFrame(self, text="Cadastrar Novo", font=("Arial", 10, "bold"), bg="#F3F4F6", padx=10, pady=10)
        self.frame_form.pack(fill="x", padx=15, pady=10)

        self.lbl_campo1 = tk.Label(self.frame_form, text="Nome:", bg="#F3F4F6")
        self.lbl_campo1.grid(row=0, column=0, padx=5)
        self.ent_campo1 = tk.Entry(self.frame_form, width=20)
        self.ent_campo1.grid(row=0, column=1, padx=5)

        self.lbl_campo2 = tk.Label(self.frame_form, text="Preço:", bg="#F3F4F6")
        self.lbl_campo2.grid(row=0, column=2, padx=5)
        self.ent_campo2 = tk.Entry(self.frame_form, width=12)
        self.ent_campo2.grid(row=0, column=3, padx=5)

        self.lbl_campo3 = tk.Label(self.frame_form, text="Quantidade:", bg="#F3F4F6")
        self.lbl_campo3.grid(row=0, column=4, padx=5)
        self.ent_campo3 = tk.Entry(self.frame_form, width=10)
        self.ent_campo3.grid(row=0, column=5, padx=5)

        tk.Button(
            self.frame_form, text="➕ Salvar", bg="#10B981", fg="white",
            font=("Arial", 9, "bold"), padx=10, command=self._salvar_item
        ).grid(row=0, column=6, padx=8)

        tk.Button(
            self.frame_form, text="🗑️ Apagar Selecionado", bg="#DC2626", fg="white",
            font=("Arial", 9, "bold"), padx=10, command=self._apagar_item
        ).grid(row=0, column=7, padx=8)

    def _ver_produtos(self):
        self.modo_atual = "produtos"
        self.lbl_campo2.config(text="Preço:")
        self.lbl_campo3.config(text="Quantidade:")
        self.carregar_dados()

    def _ver_clientes(self):
        self.modo_atual = "clientes"
        self.lbl_campo2.config(text="E-mail:")
        self.lbl_campo3.config(text="Telefone:")
        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        if self.modo_atual == "produtos":
            self.tabela.heading("c1", text="ID")
            self.tabela.heading("c2", text="Nome do Produto")
            self.tabela.heading("c3", text="Preço")
            self.tabela.heading("c4", text="Estoque")

            dados, fonte = banco.listar_produtos()
            for p in dados:
                self.tabela.insert("", "end", values=(p["id"], p["nome"], f"R$ {p['preco_unitario']}", p["quantidade_estoque"]))
        else:
            self.tabela.heading("c1", text="ID")
            self.tabela.heading("c2", text="Nome do Cliente")
            self.tabela.heading("c3", text="E-mail")
            self.tabela.heading("c4", text="Telefone")

            dados, fonte = banco.listar_clientes()
            for c in dados:
                self.tabela.insert("", "end", values=(c["id"], c["nome"], c["email"], c["telefone"]))

        if "REDIS" in fonte:
            self.lbl_fonte.config(text=f"Fonte: 🟢 {fonte} (Memória RAM instantânea)", fg="#4ADE80")
        else:
            self.lbl_fonte.config(text=f"Fonte: 🟡 {fonte} (Consultado do Supabase na Nuvem)", fg="#FACC15")

    def _salvar_item(self):
        v1 = self.ent_campo1.get().strip()
        v2 = self.ent_campo2.get().strip()
        v3 = self.ent_campo3.get().strip()

        if not v1 or not v2:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios!")
            return

        try:
            if self.modo_atual == "produtos":
                banco.criar_produto(v1, float(v2), int(v3 or 0))
                messagebox.showinfo("Sucesso", "Produto cadastrado no Supabase! Cache do Redis invalidado.")
            else:
                banco.criar_cliente(v1, v2, v3)
                messagebox.showinfo("Sucesso", "Cliente cadastrado no Supabase! Cache do Redis invalidado.")

            self.ent_campo1.delete(0, "end")
            self.ent_campo2.delete(0, "end")
            self.ent_campo3.delete(0, "end")
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _apagar_item(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item da tabela para apagar!")
            return

        item_id = self.tabela.item(selecionado[0], "values")[0]

        if self.modo_atual == "produtos":
            banco.apagar_produto(item_id)
        else:
            banco.apagar_cliente(item_id)

        messagebox.showinfo("Sucesso", "Item removido no Supabase e cache do Redis invalidado!")
        self.carregar_dados()

    def _limpar_cache(self):
        banco.limpar_cache()
        messagebox.showinfo("Cache", "Cache do Redis apagado com sucesso!\nA próxima consulta buscará do Supabase.")
        self.carregar_dados()

if __name__ == "__main__":
    app = App()
    app.mainloop()
