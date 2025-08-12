import json

with open("db.json", encoding="utf-8") as f:
    data = json.load(f)

# Filtra os perfis
profiles = [obj for obj in data if obj["model"] == "users.profile"]

# Extrai os IDs dos utilizadores referenciados
user_ids = {p["fields"]["user"] for p in profiles}

# Busca os utilizadores correspondentes
users = [obj for obj in data if obj["model"] == "auth.user" and obj["pk"] in user_ids]

# Define as outras apps que queres importar
apps_extra = {"blog.post", "blog.comment", "notifications.notification", "private_messages.message"}
resto = [obj for obj in data if obj["model"] in apps_extra]

# Junta tudo num ficheiro final
final_data = users + profiles + resto

with open("db_final_com_users.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

print("Ficheiro db_final_com_users.json criado com utilizadores, perfis e apps do projeto.")
