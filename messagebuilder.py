import botsecrets

# ИД Хамбарта
HAMBART_ID = botsecrets.HAMBART_ID

# Ссылка (шаблон) на страницу с убийством
KILLBOARD_KILL_URL = botsecrets.KILLBOARD_KILL_URL

def __map_attackers_to_attackers_ids(attacker):
    '''
    Мапа для перевода аттакеров в их ИД-шники
    '''
    try:
        return attacker['character_id']
    except Exception as e:
        # Так как бывают случаи, когда приходят данные без 'character_id'
        return 0

def __attackers_ids(json_dict):
    '''
    Получение ИД-шники аттакеров
    '''
    return list(map(__map_attackers_to_attackers_ids, json_dict['attackers']))

def __victim_id(json_dict):
    '''
    Получение ИД жертвы
    '''
    try:
        return json_dict['victim']['character_id']
    except Exception as e:
        # Возможны случаи, когда тут придут данные без 'character_id'
        return -1
    
def __ship_type_id(json_dict):
    try:
        return json_dict['victim']['ship_type_id']
    except Exception as e:
        return None

def __hambart_role(attackers_ids, victim_id):
    '''
    Получение роли Хамбарта в замесе

    Если Хамбарт убил кого-то ... то 'attacker'
    Если Хамбарт был жертвой .... то 'victim'
    Если что-то другое .......... то None
    '''
    DEBUG_HAMBART_ID = 0
    if HAMBART_ID == DEBUG_HAMBART_ID:
        return 'attacker'
    
    if HAMBART_ID in attackers_ids:
        return 'attacker'
    
    if HAMBART_ID == victim_id:
        return 'victim'
    
    return None

def __killmail_link(json_dict):
    '''
    Получение ссылки на убийство на сайте zkillboard
    '''
    try:
        killmail_id = json_dict['killmail_id']
        return f"{KILLBOARD_KILL_URL}/{killmail_id}/"
    except Exception as e:
        # На случай, если в словаре не будет 'killmail_id'
        return "Битая ссылка :С"

def __pretty_status(hambart_role):
    '''
    Форматированный статус
    '''
    if hambart_role == 'victim':
        return "💀💀 Hambart был убит 💀💀"
    elif hambart_role == 'attacker':
        return "🎉🎉 Hambart победил 🎉🎉"
    
def __pretty_details(attackers_count):
    '''
    Форматированные детали
    '''
    return f"1 vs {attackers_count}"
    
def __pretty_link(json_dict):
    '''
    Форматированная ссылка
    '''
    link = __killmail_link(json_dict=json_dict)
    return f"Ссылка : {link}"

def response(json_dict):
    '''
    Получение форматированного ответа по JSON
    '''
    attackers_ids = __attackers_ids(json_dict=json_dict)
    if not attackers_ids:
        return None

    victim_id = __victim_id(json_dict=json_dict)
    if victim_id is None:
        return None
    
    CAPSULE_SHIP_TYPE = 670
    ship_type_id = __ship_type_id(json_dict=json_dict)
    if ship_type_id == CAPSULE_SHIP_TYPE:
        return None

    hambart_role = __hambart_role(attackers_ids=attackers_ids,
                                  victim_id=victim_id)
    if hambart_role is None:
        return None
    
    attackers_count = len(attackers_ids)

    status = __pretty_status(hambart_role=hambart_role)
    details = __pretty_details(attackers_count=attackers_count)
    link = __pretty_link(json_dict=json_dict)

    killmail_response = f"{status}\n{details}\n\n{link}"

    return killmail_response
