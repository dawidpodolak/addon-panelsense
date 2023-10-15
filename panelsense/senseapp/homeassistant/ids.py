global_message_counter = 100


def get_message_id():
    global global_message_counter
    global_message_counter += 1
    return global_message_counter
