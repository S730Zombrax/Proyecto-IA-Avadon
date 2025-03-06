BLOOD_TYPES = {
    'A+': {
        'can_receive_from': ['A+', 'A-', 'O+', 'O-'],
        'can_donate_to': ['A+', 'AB+']
    },
    'A-': {
        'can_receive_from': ['A-', 'O-'],
        'can_donate_to': ['A+', 'A-', 'AB+', 'AB-']
    },
    'B+': {
        'can_receive_from': ['B+', 'B-', 'O+', 'O-'],
        'can_donate_to': ['B+', 'AB+']
    },
    'B-': {
        'can_receive_from': ['B-', 'O-'],
        'can_donate_to': ['B+', 'B-', 'AB+', 'AB-']
    },
    'AB+': {
        'can_receive_from': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'can_donate_to': ['AB+']
    },
    'AB-': {
        'can_receive_from': ['A-', 'B-', 'AB-', 'O-'],
        'can_donate_to': ['AB+', 'AB-']
    },
    'O+': {
        'can_receive_from': ['O+', 'O-'],
        'can_donate_to': ['A+', 'B+', 'AB+', 'O+']
    },
    'O-': {
        'can_receive_from': ['O-'],
        'can_donate_to': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    }
}

def get_compatibility_info(blood_type):
    if blood_type in BLOOD_TYPES:
        return BLOOD_TYPES[blood_type]
    return None
