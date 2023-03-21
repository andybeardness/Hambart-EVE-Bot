import botsecrets
import anekdot

# ИД Хамбарта
HAMBART_ID = botsecrets.HAMBART_ID

# Ссылка (шаблон) на страницу с убийством
KILLBOARD_KILL_URL = botsecrets.KILLBOARD_KILL_URL

def __map_attackers_to_attackers_ids(attacker):
    '''
    Мапа для перевода аттакеров в их ИД-шники
    '''
    return attacker['character_id']

def __attackers_ids(json_dict):
    '''
    Получение ИД-шники аттакеров
    '''
    return list(map(__map_attackers_to_attackers_ids, json_dict['attackers']))

def __victim_id(json_dict):
    '''
    Получение ИД жертвы
    '''
    return json_dict['victim']['character_id']

def __hambart_role(attackers_ids, victim_id):
    '''
    Получение роли Хамбарта в замесе

    Если Хамбарт убил кого-то, то 'attacker'
    Если Хамбарт был жертвой, то 'victim'
    Если что-то другое, то None
    '''
    if HAMBART_ID in attackers_ids:
        return 'attacker'
    
    if HAMBART_ID == victim_id:
        return 'victim'
    
    return None

def __killmail_link(json_dict):
    '''
    Получение ссылки на убийство на сайте zkillboard
    '''
    killmail_id = json_dict['killmail_id']
    return f"{KILLBOARD_KILL_URL}/{killmail_id}/"

def __pretty_status(hambart_role):
    '''
    Форматированный статус
    '''
    if hambart_role == 'victim':
        return "💀💀 Hambart был убит 💀💀"
    elif hambart_role == 'attacker':
        return "🎉🎉 Hambart одержал победу 🎉🎉"
    
def __pretty_details(hambart_role, attackers_count):
    '''
    Форматированные детали
    '''
    if hambart_role == 'victim':
        if attackers_count == 1:
            return "Славный Hambart был убит в бою 1 vs 1 👎"
        else:
            return f"Славный Hambart был убит в бою 1 vs {attackers_count} 🥴"

    elif hambart_role == 'attacker':
        if attackers_count == 1:
            return "Славный Hambart убил говноеда в бою 1 vs 1 👍"
        else:
            return f"Славный Hambart убил говноеда толпой 1 vs {attackers_count} 😊"
    
    else:
        return "В этом бою Hambart не принимал участия :С"
    
def __pretty_link(json_dict):
    '''
    Форматированная ссылка
    '''
    link = __killmail_link(json_dict=json_dict)
    return f"Ссылка на фраг : {link}"

def __pretty_anekdot():
    '''
    Форматированный анекдот
    '''
    anek = anekdot.get_anekdot()
    return f"Случайный анекдот :\n{anek}"

def response(json_dict):
    '''
    Получение форматированного ответа по JSON
    '''
    attackers_ids = __attackers_ids(json_dict=json_dict)
    victim_id = __victim_id(json_dict=json_dict)

    hambart_role = __hambart_role(attackers_ids=attackers_ids,
                                  victim_id=victim_id)
    
    if hambart_role is None:
        return None

    # hambart_role = 'attacker'

    attackers_count = len(attackers_ids)

    status = __pretty_status(hambart_role=hambart_role)
    details = __pretty_details(hambart_role=hambart_role,
                               attackers_count=attackers_count)
    link = __pretty_link(json_dict=json_dict)
    anek = __pretty_anekdot()

    resp = '\n\n'.join([status, details, link, anek])

    return resp
