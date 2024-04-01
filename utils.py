def handle_block_info(block_key, detection_unet_diffusers_keys, type="attn1"):
    block_weight_key = block_key[:block_key.find(type)+len(type)]
    real_key = None
    for __key in detection_unet_diffusers_keys:
        if block_weight_key in __key:
            real_key = detection_unet_diffusers_keys[__key]
            break
    if real_key is None:
        return (None, None, None)
    block_level = real_key.split(".")
    if block_level[0] == "input_blocks":
        block_name = "input"
        block_number = int(block_level[1])
    elif block_level[0] == "middle_block":
        block_name = "middle"
        block_number = int(block_level[1])
    elif block_level[0] == "output_blocks":
        block_name = "output"
        block_number = int(block_level[1])
    else:
        block_name = None
        block_number = 0
    attention_index = 0
    for i, v in enumerate(block_level):
        if v == "transformer_blocks":
            attention_index = int(block_level[i+1])
            break
    return (block_name, block_number, attention_index)

def save_attn(value, attn_store, block_name, block_number, attention_index):
    if attn_store is None:
        return
    if block_name not in attn_store:
        attn_store[block_name] = {}
    if block_number not in attn_store[block_name]:
        attn_store[block_name][block_number] = {}
    attn_store[block_name][block_number][attention_index] = value