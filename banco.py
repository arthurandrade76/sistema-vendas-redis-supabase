import json
from supabase import create_client
import redis

S_URL = "https://hehmkjzdjwadvtlwnbqr.supabase.co"
S_KEY = "sb_publishable_rQPIDBeyNqwHzY_CgPZx7w_Xc9iufc5"
supabase = create_client(S_URL, S_KEY)

r = redis.Redis(
    host="authentic-driftwood-meat-53255.db.redis.io",
    port=19470,
    decode_responses=True,
    username="default",
    password="lXMKlhIglVakk7QyIoQj0zUhCeqQ07OX",
)

def criar_produto(nome, preco, quantidade):
    resultado = supabase.table("produtos").insert({
        "nome": nome,
        "preco_unitario": float(preco),
        "quantidade_estoque": int(quantidade)
    }).execute().data
    r.delete("produtos")
    return resultado

def listar_produtos():
    em_cache = r.get("produtos")
    if em_cache:
        return json.loads(em_cache), "REDIS"

    produtos = supabase.table("produtos").select("*").order("id").execute().data
    r.set("produtos", json.dumps(produtos), ex=60)
    return produtos, "SUPABASE"

def atualizar_produto(id, nome, preco, quantidade):
    resultado = supabase.table("produtos").update({
        "nome": nome,
        "preco_unitario": float(preco),
        "quantidade_estoque": int(quantidade)
    }).eq("id", id).execute().data
    r.delete("produtos")
    return resultado

def apagar_produto(id):
    resultado = supabase.table("produtos").delete().eq("id", id).execute().data
    r.delete("produtos")
    return resultado

def criar_cliente(nome, email, telefone):
    resultado = supabase.table("clientes").insert({
        "nome": nome,
        "email": email,
        "telefone": telefone
    }).execute().data
    r.delete("clientes")
    return resultado

def listar_clientes():
    em_cache = r.get("clientes")
    if em_cache:
        return json.loads(em_cache), "REDIS"

    clientes = supabase.table("clientes").select("*").order("id").execute().data
    r.set("clientes", json.dumps(clientes), ex=60)
    return clientes, "SUPABASE"

def atualizar_cliente(id, nome, email, telefone):
    resultado = supabase.table("clientes").update({
        "nome": nome,
        "email": email,
        "telefone": telefone
    }).eq("id", id).execute().data
    r.delete("clientes")
    return resultado

def apagar_cliente(id):
    resultado = supabase.table("clientes").delete().eq("id", id).execute().data
    r.delete("clientes")
    return resultado

def limpar_cache():
    r.delete("produtos", "clientes")
