usuarios = {
  "11122233301": ["Samuel", "0x66d7247e"],
  "44455566602": ["Abilio", "0xe6877603"],
  "12345678900": ["Visitante", None]
}

def find_user_by_cpf(cpf):
    if cpf in usuarios:
        nome, rfid = usuarios[cpf]
        return nome, cpf
    return None, None

def find_user_by_rfid(rfid_tag):
    for cpf, (nome, rfid) in usuarios.items():
        if rfid == rfid_tag:
            return nome, cpf
    return None, None