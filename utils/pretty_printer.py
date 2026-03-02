def print_header(title):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def print_section(title):
    print("\n" + "-"*60)
    print(f"{title}")
    print("-"*60)

def print_list(items, indent=2):
    for i in items:
        print(" " * indent + str(i))

def print_kv(key, value):
    print(f"{key:<25}: {value}")