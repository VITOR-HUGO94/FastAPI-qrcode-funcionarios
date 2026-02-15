import sys
from app.database import SessionLocal
from app.models import User
from app.auth import gerar_hash_senha

def create_initial_admin(username, password):
    db = SessionLocal()
    try:
        # Verifica se o usuário já existe
        user_exists = db.query(User).filter(User.username == username).first()
        if user_exists:
            print(f"⚠️ Erro: Usuário '{username}' já existe no sistema.")
            return

        # Cria o novo admin
        new_admin = User(
            username=username,
            hashed_password=gerar_hash_senha(password)
        )
        db.add(new_admin)
        db.commit()
        print(f"✅ Sucesso: Administrador '{username}' criado com sucesso!")
    
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Pegamos os argumentos via terminal: python create_admin.py <user> <pass>
    if len(sys.argv) < 3:
        print("Uso: python -m app.create_admin <username> <password>")
    else:
        create_initial_admin(sys.argv[1], sys.argv[2])